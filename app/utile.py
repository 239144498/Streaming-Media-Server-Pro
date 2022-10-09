#!/usr/bin python3
# -*- coding: utf-8 -*-
# @Author: Naihe
# @Email: 239144498@qq.com
# @Software: Streaming-Media-Server-Pro
import asyncio
import datetime
import re
import time

from urllib.parse import quote
from loguru import logger
from threading import Thread
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from app.common.endecrypt import get4gtvurl
from app.common.gitrepo import agit
from app.common.generateEpg import postask, generateprog
from app.common.tools import genftlive, now_time, solvelive, generate_url, gdata
from app.modules.DBtools import redisState, cur, DB
from app.modules.request import request
from app.settings import xmlaccess_token, xmlowner, xmlrepo, PATH, localhost, repoState, HD, \
    repoowner, idata, downurls, vbuffer, downchoose


class container:
    def __init__(self):
        self.repo = None
        self.para = {}
        self.filename = {}  # -1->redis | 0->downloading | 1->completed
        self.owner = repoowner

        if redisState:
            # 读取redis数据到内存
            keys = cur.keys()
            _ = []
            for k in keys:  # 排除非电视节目
                if "4gtv" in str(k) or "litv" in str(k):
                    _.append(k)
            for key, value in zip(_, cur.mget(_)):
                _ = eval(value)
                if len(_) < 3:
                    continue
                self.updatelocal(key, _)

        logger.success("init final")

    def updateonline(self, fid, hd):
        status_code, url, data = get4gtvurl(fid, hd)
        start = time.time()
        if status_code == 200:
            last = int(re.findall(r"expires.=(\d+)", url).pop())
            seq, gap = genftlive(data)
            if redisState:
                cur.setex(fid, last - now_time(), str([url, last, start, seq, gap]))
            self.para[fid] = {
                "url": url,
                "last": last,
                "start": start,
                "seq": seq,
                "gap": gap
            }
            return 200
        elif status_code == 429:
            if "/second" in data:
                idata[fid]["lt"] = now_time() + 1
            elif "/day" in data:
                idata[fid]["lt"] = now_time() + 3600
        elif status_code > 503:
            idata[fid]["lt"] = now_time() + 60
        elif status_code == 403:
            idata[fid]["lt"] = now_time() + 3
        else:
            idata[fid]["lt"] = now_time() + 60
        return 404

    def updatelocal(self, fid, _):
        self.para[fid] = {
            "url": _[0],
            "last": _[1],
            "start": _[2],
            "seq": _[3],
            "gap": _[4]
        }
        return 200

    def check(self, fid, hd):
        """
        处理参数
        :param fid:
        :param hd:
        :return:
        """
        code = 200
        if not self.para.get(fid) or self.para.get(fid)['last'] - now_time() < 0:  # 本地找
            if redisState:
                _temp = cur.get(fid)
                if not _temp or eval(_temp)[1] - now_time() < 0:  # redis找
                    code = self.updateonline(fid, hd)
                else:  # 找到放进内存
                    _ = eval(_temp)
                    code = self.updatelocal(fid, _)
            else:
                code = self.updateonline(fid, hd)
        return code


    def generalfun(self, fid, hd):
        """
        通用生成参数
        :param fid:
        :param hd:
        :return:
        """
        data = self.para.get(fid)
        if "4gtv-4gtv" in fid or "litv-ftv10" in fid or "litv-longturn17" == fid or "litv-longturn18" == fid:
            url = idata[fid][hd]
            now = now_time()
            seq = round((now - data['start']) / idata[fid]['x']) - 1
            begin = (seq + data['seq']) * idata[fid]['x']
            return data["gap"], (begin - idata[fid]['x1']) // idata[fid]['x'], url, begin
        if "4gtv-live" in fid:
            token = re.findall(r"(token1=.*&expires1=\d+)&", data['url']).pop()
            url = idata[fid]['url'] + "?" + token
            now = now_time()
            seq = solvelive(now, data['start'], data['seq'], idata[fid]['x']) - 1
            return data["gap"], seq, url, 0
        if "4gtv-ftv" in fid:
            url = idata[fid][hd]
            now = now_time()
            seq = solvelive(now, data['start'], data['seq'], idata[fid]['x']) - 1
            return data["gap"], seq, url, 0

    def generatem3u8(self, host, fid, hd):
        code = self.check(fid, hd)
        if code == 404:
            return "404"
        gap, seq, url, begin = self.generalfun(fid, hd)
        yield f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:{gap}
#EXT-X-ALLOW-CACHE:YES
#EXT-X-MEDIA-SEQUENCE:{seq}
#EXT-X-INDEPENDENT-SEGMENTS"""
        for num1 in range(5):
            yield f"\n#EXTINF:{idata[fid]['gap']}" \
                  + "\n" + generate_url(fid, host, hd, begin + (num1 * idata[fid]['x']), seq + num1, url)

    def new_generatem3u8(self, host, fid, hd, background_tasks):
        code = self.check(fid, hd)
        if code == 404:
            return "404"
        gap, seq, url, begin = self.generalfun(fid, hd)
        if downchoose == "online":
            background_tasks.add_task(backtaskonline, url, fid, seq, hd, begin, host)
        elif downchoose == "local":
            background_tasks.add_task(backtasklocal, url, fid, seq, hd, begin, host)
        yield f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:{gap}
#EXT-X-MEDIA-SEQUENCE:{seq}
#EXT-X-INDEPENDENT-SEGMENTS"""
        tsname = fid + str(seq) + ".ts"
        if tsname in self.filename and self.filename.get(tsname) == 1:
            for num1 in range(vbuffer):
                url = "\n" + localhost + f"/call.ts?fid={fid}&seq={str(seq + num1)}&hd={hd}"
                yield f"\n#EXTINF:{idata[fid]['gap']}" + url
        else:
            for num1 in range(1):
                url = "\n" + localhost + f"/call.ts?fid={fid}&seq={str(seq + num1)}&hd={hd}"
                yield f"\n#EXTINF:{idata[fid]['gap']}" + url

    def geturl(self, fid, hd):
        code = self.check(fid, hd)
        if code == 404:
            return "https://github.com/239144498/Streaming-Media-Server-Pro"
        if "4gtv-live" not in fid:
            return re.sub(r"(\w+\.m3u8)", "channel3.m3u8", self.para[fid]['url'])
        else:
            return re.sub(r"(\w+\.m3u8)", HD[hd], self.para[fid]['url'])


get = container()


def call_get(url, tsname):
    with request.get(url) as res:
        get.filename.update({tsname: 1})


def backtaskonline(url, fid, seq, hd, begin, host):
    threads = []
    # 分布式下载，改成你的链接，看不懂就去看我发布的教程
    # urlset = ["https://www.example1.com/url3?url=", "https://www.example2.com/url3?url=",
    #           "https://www.example3.com/url3?url=", "https://www.example4.com/url3?url=",
    #           "https://www.example5.com/url3?url="]
    urlset = downurls
    for i in range(0, vbuffer):
        tsname = fid + str(seq + i) + ".ts"
        # .ts已下载或正在下载
        if tsname in get.filename:
            continue
        get.filename.update({tsname: 0})
        herf = generate_url(fid, host, hd, begin + (i * idata[fid]['x']), seq + i, url)
        x = urlset.pop() + quote(herf) + f"&filepath={tsname}"
        t = Thread(target=call_get, args=(x, tsname))
        threads.append(t)
    for index, element in enumerate(threads):
        element.start()
        time.sleep(1 + index * 0.1)
    for t in threads:
        t.join()


def backtasklocal(url, fid, seq, hd, begin, host):
    threads = []
    # 本地多线程下载
    for i in range(0, vbuffer):
        tsname = fid + str(seq + i) + ".ts"
        # .ts已下载或正在下载
        if tsname in get.filename:
            continue
        get.filename.update({tsname: 0})
        herf = generate_url(fid, host, hd, begin + (i * idata[fid]['x']), seq + i, url)
        t = Thread(target=downvideo, args=(herf, tsname))
        threads.append(t)
    for index, element in enumerate(threads):
        element.start()
        time.sleep(1.2 + index * 0.1)
    for t in threads:
        t.join()


def downvideo(url: str, filepath: str):
    """
    本地下载存放到数据库
    :param url:
    :param filepath:
    :return:
    """
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept-Encoding": "gzip, deflate, br",
    }
    a = time.time()
    repo = str(datetime.date.today())
    with request.get(url=url, headers=header) as res:
        status = res.status_code
        content = res.content
        b = time.time()
        sql = "insert into video(vname, vcontent, vsize) values(%s, %s, %s)"
        a1 = DB(0).execute(sql, (filepath, content, len(content)))  # 执行sql语句
        get.filename.update({filepath: 1})
        c = time.time()
        return {
            "总时长": round(c - a, 2),
            "请求": round(b - a, 2),
            "请求状态": status,
            "上传": round(c - b, 2),
            "上传状态": a1,
            "字长": len(content),
            "repo": repo
        }


def gotask():
    get.filename.clear()
    if repoState:
        import platform
        if "Windows" in platform.platform():
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            asyncio.run(postask())
        else:
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            loop = asyncio.get_event_loop()
            task = asyncio.ensure_future(postask())
            loop.run_until_complete(asyncio.wait([task]))

        content = generateprog(gdata)
        filepath = "4gtvchannel.xml"
        agit(xmlaccess_token).update_repo_file(xmlowner, xmlrepo, filepath, content)
        with open(PATH / "assets/EPG.xml", "wb") as f:
            f.write(content)
    logger.success("今日任务完成")


def sqltask():
    # 保留最近100条缓存，避免长时间运行内存溢出
    keys = list(get.filename)
    keys.reverse()
    _ = {}
    if len(keys) > 100:
        for index, element in enumerate(keys):
            if index < 100:
                _.update({element: get.filename.get(element)})
        get.filename = _
    logger.success("删除完成")


def everyday(t=2):
    executors = {
        'default': ThreadPoolExecutor(5),  # 名称为“default ”的ThreadPoolExecutor，最大线程20个
        'processpool': ProcessPoolExecutor(2)  # 名称“processpool”的ProcessPoolExecutor，最大进程5个
    }
    job_defaults = {
        'coalesce': False,  # 默认为新任务关闭合并模式（）
        'max_instances': 3  # 设置新任务的默认最大实例数为3
    }
    scheduler = BlockingScheduler(timezone='Asia/Shanghai', executors=executors, job_defaults=job_defaults)
    scheduler.add_job(gotask, 'cron', max_instances=10, day_of_week='0-6', hour=t, minute=00, second=00,
                      misfire_grace_time=120)
    scheduler.add_job(func=sqltask, max_instances=10, trigger=IntervalTrigger(minutes=59), misfire_grace_time=120)
    logger.info(scheduler.get_jobs())
    scheduler.start()
