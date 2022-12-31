# -*- coding: utf-8 -*-
# @Time    : 2022/10/9
# @Author  : Naihe
# @Email   : 239144498@qq.com
# @File    : more.py
# @Software: PyCharm
import urllib
from base64 import b64decode

import aiohttp
from fastapi import APIRouter, Query, Response
from fastapi.responses import FileResponse
from fastapi.requests import Request
from starlette.responses import StreamingResponse
from app.plugins.a4gtv.more_util import parse, processing, splicing
from app.conf import config
from app.conf.config import headers
from app.scheams.response import Response200, Response400


more = APIRouter(tags=["更多频道"])


@more.get('/diychannel.m3u', summary="自定义IPTV频道")
async def diychannel():
    """
    新版接口
    不止于4gtv,还可以添加更多频道到程序中,未来将推出代理自定义频道功能
    """
    filename = config.ROOT / "assets/diyepg.txt"
    return FileResponse(path=filename, status_code=200, headers={
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Content-Type': 'application/vnd.apple.mpegurl'
    })


@more.get('/proxy', summary="代理任意m3u8")
async def proxy(request: Request, url: str = Query(..., regex=config.url_regex)):
    """
    可代理任意m3u8链接，解决网站播放其他域名链接出现的跨域问题，解决封锁地区问题等等
    - **url**: m3u8链接
    - url example1：/proxy?url=https://example.com/cctv1.m3u8
    - url example2编码处理：/proxy?url=https%3A%2F%2Fexample.com%2Fcctv1.m3u8%3Ftoken%3D123456
    """
    url = dict(request.query_params)
    if url.get("url"):
        url = parse(url)
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"
            }
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url=url, allow_redirects=True) as res:
                    data = await res.text()
                    return StreamingResponse(processing(url, iter(data.split("\n"))))
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            return Response400(data=str(e))
    return Response400(data="None")


@more.get('/pdl', summary="代理下载")
async def pdl(request: Request, url: str = Query(...)):
    """
    可代理任意m3u8链接，解决网站播放其他域名链接出现的跨域问题，解决封锁地区问题等等
    - **url**: 视频链接
    """
    url = b64decode(url.encode("utf-8")).decode("utf-8")
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Upgrade-Insecure-Requests": "1",
    }
    async with aiohttp.ClientSession(headers=header) as session:
        async with session.get(url=url) as res:
            return Response(content=await res.read(), status_code=200, headers=headers, media_type='video/MP2T')


@more.get('/count', summary="统计")
async def count1():
    """
    统计使用次数
    """
    return Response200(data=str(config.count))


