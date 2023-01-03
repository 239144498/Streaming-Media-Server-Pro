#!/usr/bin python3
# -*- coding: utf-8 -*-
import base64
import time
import datetime
import requests

from loguru import logger
from threading import Thread
from urllib.parse import urlparse, urljoin

from app.conf.config import config, request, gdata
from app.plugins.a4gtv.endecrypt import get4gtvurl
from app.common.header import random_header
from app.conf.config import repoowner, default_cfg, localhost, vbuffer, \
    mysql_cfg, downurls
from app.db.DBtools import redisState, cur, DBconnect
from app.db.localfile import vfile
from app.plugins.a4gtv.tools import now_time, safe_int, generate_url


class container:
    def __init__(self):
        self.para = {}
        self.filename = {}
        self.owner = repoowner
        self.idata = {}
        self.init()

    def init(self):
        if redisState:
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

    def updateonline(self, fid):
        status_code, a6, a12, a1, msg = get4gtvurl(fid)
        if (status_code == 200 or abs(status_code - 300) < 10) and "成功" in msg:
            a10, a11, a3, a2, a7, a8, a9 = list(map(safe_int, ''.join([chr(ord(i) + 2) for i in base64.b64decode(a12).decode("utf-8")[::-1]]).split(':')))
            self.updatelocal(fid, [a1, a2, a3, a11 + a10, a10 / -a1, a6, a7, a8, a9])
            config.count += 1
            if redisState:
                cur.setex(fid, a2 - a1, str([a1, a2, a3, a11 + a10, a10 / -a1, a6, a7, a8, a9]))
            return 200
        elif abs(status_code - 503) < 10:  # 服务器维护
            self.idata[fid]["lt"] = a1 + 30
        elif status_code == 403:  # 链接失效
            self.idata[fid]["lt"] = a1 + 60
        elif status_code == 229:  # 频率过快
            self.idata[fid]["lt"] = a1 + 3
        elif status_code == 230:  # 接口每日上限
            self.idata[fid]["lt"] = a1 + 3600
        elif status_code == 216:
            logger.error("该ip已被程序拉黑，无法访问")
            logger.error("了解封禁规则https://github.com/239144498/Streaming-Media-Server-Pro/issues/14")
            exit(-1)
        elif status_code == 410:  # 过期
            self.idata[fid]["lt"] = a1 + 3
        elif status_code == 411:  # 验证失败 升级最新版解决
            logger.warning("请升级到最新版")
            self.idata[fid]["lt"] = a1 + 999
        else:  # 其他情况
            self.idata[fid]["lt"] = a1 + 120
        logger.warning("未获得数据")
        logger.warning(f"{status_code}, {a12}")
        return 404

    def updatelocal(self, fid, _):
        self.para[fid] = {
            "a1": _[0],
            "a2": _[1],
            "a3": _[2],
            "a4": _[3],
            "a5": _[4],
            "a6": _[5],
            "a7": _[6],
            "a8": _[7],
            "a9": _[8],
        }
        return 200

    def check(self, fid):
        """
        处理参数
        :param fid:
        :return:
        """
        code = 200
        if not self.para.get(fid) or self.para.get(fid)['a2'] - now_time() < 0:
            if redisState:
                _temp = cur.get(fid)
                if not _temp or eval(_temp)[1] - now_time() < 0:
                    code = self.updateonline(fid)
                else:
                    _ = eval(_temp)
                    code = self.updatelocal(fid, _)
            else:
                code = self.updateonline(fid)
        return code

    def generalfun(self, fid):
        """
        通用生成参数
        :param fid:
        :param hd:
        :return:
        """
        data = self.para.get(fid)
        if "4gtv-4gtv" in fid or "litv-ftv10" in fid or "litv-longturn17" == fid or "litv-longturn18" == fid:
            url = self.para[fid]["a8"] + "?" + data["a9"]
            now = now_time()
            seq = round(data["a4"] + now * data["a5"]) + data["a3"]
            begin = data["a7"] * round(data["a4"] + now * data["a5"]) + data["a3"]
            return data["a7"], seq, url, begin
        if "4gtv-live" in fid:
            url = self.para[fid]["a8"] + "?" + data["a9"]
            now = now_time()
            seq = round(data["a4"] + now * data["a5"]) + data["a3"]
            return data["a7"], seq, url, 0
        if "litv-ftv" in fid or "litv-longturn" in fid:
            url = self.para[fid]["a8"] + "?" + data["a9"]
            now = now_time()
            seq = round(data["a4"] + now * data["a5"]) + data["a3"]
            return data["a7"], seq, url, 0

    def generatem3u8(self, host, fid, hd):
        gap, seq, url, begin = self.generalfun(fid)
        yield f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:{gap}
#EXT-X-ALLOW-CACHE:YES
#EXT-X-MEDIA-SEQUENCE:{seq}
#EXT-X-INDEPENDENT-SEGMENTS"""
        for num1 in range(5):
            yield f"\n#EXTINF:{self.para[fid]['a7']}," \
                  + "\n" + generate_url(fid, host, begin + (num1 * self.para[fid]['a7']), seq + num1, url)
        logger.success(fid + " m3u8 generated successfully")

    def new_generatem3u8(self, host, fid, hd, background_tasks):
        gap, seq, url, begin = self.generalfun(fid)
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
                url = "\n" + urljoin(localhost, f"call.ts?fid={fid}&seq={seq + num1}&hd={hd}")
                yield f"\n#EXTINF:{self.para[fid]['a7']}," + url
        else:
            for num1 in range(1):
                url = "\n" + urljoin(localhost, f"call.ts?fid={fid}&seq={seq + num1}&hd={hd}")
                yield f"\n#EXTINF:{self.para[fid]['a7']}," + url
        logger.success(fid + " m3u8 generated successfully")

    def geturl(self, fid, hd):
        return f"{self.para[fid]['a6']}?fid={fid}&hd={hd}&type=rd"


get = container()


def call_get(url, data):
    with request.post(url, json=data, timeout=10) as res:
        get.filename.update({data['filepath']: 1})
        logger.info((data['filepath'], url[:20], res.text))


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
        herf = generate_url(fid, host, begin + (i * get.para[fid]['a7']), seq + i, url)
        x = urlset.pop()
        data = {
            "f": herf,
            "g": tsname,
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
        herf = generate_url(fid, host, begin + (i * get.para[fid]['a7']), seq + i, url)
        t = Thread(target=downvideo, args=(herf, tsname))
        threads.append(t)
        logger.info('启动downvideo完成')
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
    logger.debug('开始下载视频')
    with requests.get(url=url, headers=header, timeout=10) as res:
        status = res.status_code
        content = res.content
        logger.debug('完成下载视频')
        b = time.time()
        # 保存到mysql数据库
        if default_cfg.get("defaultdb") == "mysql":
            sql = "insert into video(vname, vcontent, vsize) values(%s, %s, %s)"
            a1 = DBconnect.execute(sql, (filepath, content, len(content)))  # 执行sql语句
        # 保存到本地硬盘
        else:
            a1 = vfile.file_store(filepath, content)
        logger.debug('保存视频完成')

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
