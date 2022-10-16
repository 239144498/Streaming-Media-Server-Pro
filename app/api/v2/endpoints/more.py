# -*- coding: utf-8 -*-
# @Time    : 2022/10/9
# @Author  : Naihe
# @Email   : 239144498@qq.com
# @File    : more.py
# @Software: PyCharm
from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.conf import config

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

