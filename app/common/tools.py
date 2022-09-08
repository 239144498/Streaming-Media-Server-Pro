#!/usr/bin python3
# -*- coding: utf-8 -*-
import re
import time

from app.common.diyEpg import return_diyepg
from app.modules.request import request
from app.settings import gdata, localhost, tvglogo


def generate_m3u(host, hd, name):
    """
    构造 m3u 数据
    :param host:
    :param hd:
    :param name: online | channel | channel2
    :return:
    """
    name += ".m3u8"
    yield '#EXTM3U x-tvg-url=""\n'
    for i in gdata:
        # tvg-ID="" 频道id匹配epg   fsLOGO_MOBILE 台标 | fsHEAD_FRAME 播放预览
        yield '#EXTINF:{} tvg-chno="{}" tvg-id="{}" tvg-name="{}" tvg-logo="{}" group-title="{}",{}\n'.format(
            -1, i['fs4GTV_ID'], i['fs4GTV_ID'], i['fsNAME'], i[tvglogo], i['fsTYPE_NAME'], i['fsNAME'])
        if not host:
            yield localhost + f"/{name}?fid={i['fs4GTV_ID']}&hd={hd}\n"
        else:
            yield localhost + f"/{name}?fid={i['fs4GTV_ID']}&hd={hd}&host={host}\n"
    yield return_diyepg()  # 返回自定义频道


def writefile(filename, content):
    with open(filename, "wb") as f:
        f.write(content)
        f.close()


def get_4gtv(url):
    header = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    with request.get(url=url, headers=header) as res:
        return res.text


def solvelive(now, t1, t2, gap):
    x = now - t1
    seq = round(t2 + x // gap)
    return seq


def genftlive(url):
    start = time.time()
    data = get_4gtv(url)
    seq = re.findall("#EXT-X-MEDIA-SEQUENCE:(\d+)\n", data).pop()
    gap = re.findall("#EXT-X-TARGETDURATION:(\d+)\n", data).pop()
    return start, int(seq), int(gap)


def generate_url(fid, host, hd, begin, seq, url):
    if "4gtv-4gtv" in fid or "-ftv10" in fid or "-longturn17" in fid or "-longturn18" in fid:
        return url.format(host, begin, seq)
    elif "4gtv-live" in fid:
        return url.format(host, fid, f"{hd}{seq}")
    else:
        return url.format(host, seq)


def now_time():
    return int(time.time())

