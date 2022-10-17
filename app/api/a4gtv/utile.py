#!/usr/bin python3
# -*- coding: utf-8 -*-
import datetime
import re
import time

from threading import Thread
from urllib.parse import urlparse, urljoin

import asyncio
import requests
from loguru import logger

from app.api.a4gtv.endecrypt import get4gtvurl
from app.api.a4gtv.tools import genftlive, now_time, generate_url, solvelive
from app.common.gitrepo import agit, request
from app.common.header import random_header
from app.conf.config import repoowner, repoaccess_token, repoState, idata, default_cfg, localhost, vbuffer, \
    HD, mysql_cfg, downurls
from app.db.DBtools import redisState, cur, DBconnect


class container:
    def __init__(self):
        self.repo = None
        self.para = {}
        self.filename = {}  # -1->redis | 0->downloading | 1->completed
        self.owner = repoowner
        Thread(target=self.init).start()

    def inin_repo(self):
        logger.info("开始初始化")
        self.repo = str(datetime.date.today())
        state = agit(repoaccess_token).cat_repo(self.owner, self.repo)
        if state == 404:
            agit(repoaccess_token).create_repo(self.repo)
            logger.success(f"创建repo {self.repo} 完成")

    def init(self):
        if repoState:
            self.inin_repo()
            # 读取已上传到agit的文件名到内存
            reposha = agit(repoaccess_token).get_repo_sha(self.owner, self.repo)
            for i in agit(repoaccess_token).cat_repo_tree(self.owner, self.repo, reposha)['tree']:
                if i["size"] >= 5000 and ".ts" in i["path"]:
                    self.filename.update({i["path"]: -1})

        if redisState:
            # 读取redis数据到内存
            keys = cur.keys()
            _ = []
            for k in keys:  # 排除非电视节目
                if "4gtv" in str(k) or "litv" in str(k):
                    _.append(k)
            for key, value in zip(_, cur.mget(_)):
                _ = eval(value)
                if type(_) is not list or len(_) < 3:
                    continue
                self.updatelocal(key, _)

        logger.success("init final")

    def updateonline(self, fid, _=0):
        status_code, url, data, start = get4gtvurl(fid)
        url2 = re.findall(r"((http|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&:/~\+#]*[\w\-\@?^=%&/~\+#])?)", data).pop()[0]
        if (status_code == 200 or abs(status_code - 300) < 10) and "#EXTM3U" in data:
            if "4gtv-live" not in fid:
                _ = 3600 * 23
            last = int(re.findall(r"expires.=(\d+)", url).pop()) + _
            seq, gap = genftlive(data)
            self.updatelocal(fid, [url2, last, start, seq, gap])
            if redisState:
                cur.setex(fid, last - start, str([url2, last, start, seq, gap]))
            return 200
        elif abs(status_code - 503) < 10:   # 服务器维护
            idata[fid]["lt"] = start + 20
        elif status_code == 403:    # 链接失效
            idata[fid]["lt"] = start + 3
        else:   # 其他情况
            idata[fid]["lt"] = start + 10
        logger.warning("未获得有效数据")
        logger.warning(f"{status_code}, {url}, {data}")
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

    def check(self, fid):
        """
        处理参数
        :param fid:
        :return:
        """
        code = 200
        if not self.para.get(fid) or self.para.get(fid)['last'] - now_time() < 0:  # 本地找
            if redisState:
                _temp = cur.get(fid)
                if not _temp or eval(_temp)[1] - now_time() < 0:  # redis找
                    code = self.updateonline(fid)
                else:  # 找到放进内存
                    _ = eval(_temp)
                    code = self.updatelocal(fid, _)
            else:
                code = self.updateonline(fid)
        return code

    def generalfun(self, fid, hd, x=0):
        """
        通用生成参数
        :param fid:
        :param hd:
        :return:
        """
        if "4gtv-4gtv073" == fid:
            x = 110
        data = self.para.get(fid)
        token = "?" + urlparse(data['url']).query
        if "4gtv-4gtv" in fid or "litv-ftv10" in fid or "litv-longturn17" == fid or "litv-longturn18" == fid:
            url = idata[fid][hd] + token
            now = now_time()
            seq = round((now - data['start']) / idata[fid]['x']) - 2 + x
            begin = (seq + data['seq']) * idata[fid]['x']
            return data["gap"], (begin - idata[fid]['x1']) // idata[fid]['x'], url, begin
        if "4gtv-live" in fid:
            url = idata[fid]['url'] + token
            now = now_time()
            seq = solvelive(now, data['start'], data['seq'], idata[fid]['x']) - 5
            return data["gap"], seq, url, 0
        if "litv-ftv" in fid or "litv-longturn" in fid:
            url = idata[fid][hd] + token
            now = now_time()
            seq = solvelive(now, data['start'], data['seq'], idata[fid]['x']) - 2
            return data["gap"], seq, url, 0

    def generatem3u8(self, host, fid, hd):
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
        gap, seq, url, begin = self.generalfun(fid, hd)
        if default_cfg.get("downchoose") == "online":
            background_tasks.add_task(backtaskonline, url, fid, seq, hd, begin, host)
        elif default_cfg.get("downchoose") == "local":
            background_tasks.add_task(backtasklocal, url, fid, seq, hd, begin, host)
        yield f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:{gap}
#EXT-X-MEDIA-SEQUENCE:{seq}
#EXT-X-INDEPENDENT-SEGMENTS"""
        tsname = fid + str(seq) + ".ts"
        if tsname in self.filename and self.filename.get(tsname) == 1:
            for num1 in range(vbuffer):
                url = "\n" + urljoin(localhost, f"call.ts?fid={fid}&seq={str(seq + num1)}&hd={hd}")
                yield f"\n#EXTINF:{idata[fid]['gap']}" + url
        else:
            for num1 in range(1):
                url = "\n" + urljoin(localhost, f"call.ts?fid={fid}&seq={str(seq + num1)}&hd={hd}")
                yield f"\n#EXTINF:{idata[fid]['gap']}" + url

    def geturl(self, fid, hd):
        return re.sub(r"(\w+\.m3u8)", HD[hd], self.para[fid]['url'])


get = container()


def call_get(url, data):
    with request.post(url, json=data) as res:
        get.filename.update({data['filepath']: 1})
        logger.info((data['filepath'], url[:20], res.text))


def backtaskonline(url, fid, seq, hd, begin, host):
    threads = []
    # 分布式下载，改成你的链接，看不懂就去看我发布的教程
    # urlset = ["https://www.example1.com/url3?url=", "https://www.example2.com/url3?url=",
    #           "https://www.example3.com/url3?url=", "https://www.example4.com/url3?url=",
    #           "https://www.example5.com/url3?url="]
    urlset = downurls
    # random.shuffle(urlset)
    for i in range(0, vbuffer):
        tsname = fid + str(seq + i) + ".ts"
        # .ts已下载或正在下载
        if tsname in get.filename:
            continue
        get.filename.update({tsname: 0})
        herf = generate_url(fid, host, hd, begin + (i * idata[fid]['x']), seq + i, url)
        x = urlset.pop()
        data = {
            "url": herf,
            "filepath": tsname,
            'a': mysql_cfg["host"],
            'b': mysql_cfg["user"],
            'c': mysql_cfg["password"],
            'd': int(mysql_cfg["port"]),
            'e': mysql_cfg["database"],
        }
        t = Thread(target=call_get, args=(x, data))
        threads.append(t)
    for index, element in enumerate(threads):
        element.start()
        time.sleep(1 + index * 0.1)


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
        time.sleep(1 + index * 0.1)


def downvideo(url: str, filepath: str):
    """
    本地下载存放到数据库
    :param url:
    :param filepath:
    :return:
    """
    header = {
        "User-Agent": random_header(),
        "Accept-Encoding": "gzip, deflate, br",
    }
    a = time.time()
    repo = str(datetime.date.today())
    with requests.get(url=url, headers=header) as res:
        status = res.status_code
        print(status)
        content = res.content
        b = time.time()
        sql = "insert into video(vname, vcontent, vsize) values(%s, %s, %s)"
        a1 = DBconnect.execute(sql, (filepath, content, len(content)))  # 执行sql语句
        get.filename.update({filepath: 1})
        c = time.time()
        return {
            "总时长": round(c - a, 2),
            "请求": round(b - a, 2),
            "请求状态": status,
            "上传": round(c - b, 2),
            "上传状态": a1,
            "字节": len(content),
            "repo": repo
        }
