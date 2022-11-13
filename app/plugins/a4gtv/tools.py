#!/usr/bin python3
# -*- coding: utf-8 -*-
import re
import time

from loguru import logger

from app.common.request import request
from app.conf.config import gdata, host1, host2, tvglogo
from urllib.parse import urljoin


def generate_m3u(host, hd, name):
    """
    构造 m3u 数据
    :param host:
    :param hd:
    :param name: online | channel | channel2
    :return:
    """
    yield '#EXTM3U x-tvg-url=""\n'
    for i in gdata:
        # tvg-ID="" 频道id匹配epg   fsLOGO_MOBILE 台标 | fsHEAD_FRAME 播放预览
        yield '#EXTINF:{} tvg-chno="{}" tvg-id="{}" tvg-name="{}" tvg-logo="{}" group-title="{}",{}\n'.format(
            -1, i['fnCHANNEL_NO'], i['fs4GTV_ID'], i['fsNAME'], i[tvglogo], i['fsTYPE_NAME'], i['fsNAME'])
        yield urljoin(host, f"{name}?fid={i['fs4GTV_ID']}&hd={hd}") + "\n"
    logger.success(name + " m3u generated successfully")


def writefile(filename, content):
    with open(filename, "wb") as f:
        f.write(content)


def get_4gtv(url):
    header = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    }
    with request.get(url=url, headers=header) as res:
        return res.text


def solvelive(now, t1, t2, gap):
    x = now - t1
    seq = round(t2 + x // gap)
    return seq


def genftlive(data):
    seq = re.findall(r"#EXT-X-MEDIA-SEQUENCE:(\d+)\n", data).pop()
    gap = re.findall(r"#EXT-X-TARGETDURATION:(\d+)\n", data).pop()
    return int(seq), int(gap)


def generate_url(fid, host, hd, begin, seq, url):
    # host 可自定义，为空时使用默认参数
    if "4gtv-4gtv" in fid or "-ftv10" in fid or "-longturn17" in fid or "-longturn18" in fid:
        return urljoin(host or host1, url.format(begin, seq))
    elif "4gtv-live" in fid:
        return urljoin(host or host2, url.format(fid, f"{hd}{seq}"))
    else:
        return urljoin(host or host1, url.format(seq))


def now_time(_=None):
    if _:
        return time.time()
    else:
        return int(time.time())
