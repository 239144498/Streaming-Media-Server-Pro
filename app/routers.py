#!/usr/bin python3
# -*- coding: utf-8 -*-
# @Author: Naihe
# @Email: 239144498@qq.com
# @Software: Streaming-Media-Server-Pro
import time
import asyncio
from typing import Any
from fastapi.responses import StreamingResponse, RedirectResponse, Response, PlainTextResponse
from fastapi import FastAPI, Query, BackgroundTasks
from app.common.tools import generate_m3u, writefile, now_time
from app.modules.DBtools import DBconnect
from app.modules.request import request
from app.scheams.basic import Response200, Response404
from app.utile import get, backtaskonline, backtasklocal
from app.settings import headers, PORT, PATH, host1, host2, localhost, downchoose, defaultdb, describe, idata


app = FastAPI(title='流媒体服务专业版',
              version="1.2.1",
              description=describe)


@app.get('/')
async def index():
    return Response200(data="Hello World!")


@app.get('/online.m3u8')
async def online(
        background_tasks: BackgroundTasks,
        host: Any = Query(None),
        fid: Any = Query(...),
        hd: Any = Query("1080")):
    """
    最新版 api v3
    该版本具有redis缓存，视频中转缓存处理等优点,直白说就是播放稳定不卡顿，看超清、4k不是问题
    :param background_tasks:
    :param host:
    :param fid:
    :param hd:
    :return:
    """
    if defaultdb == "":
        return Response404(data="请先连接数据库")
    if not (fid in idata):
        return Response404(data=f"Not found {fid}")
    t = idata[fid].get("lt", 0) - now_time()
    if t > 0:
        return Response404(data=f"{fid} 频道暂不可用，请过 {t} 秒后再试")
    if not host:
        if "4gtv-live" in fid:
            host = "https://" + host2
        else:
            host = "https://" + host1
    return StreamingResponse(get.new_generatem3u8(host, fid, hd, background_tasks), 200, {
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        'Content-Type': 'application/vnd.apple.mpegurl',
    })


@app.get('/call.ts')
async def call(background_tasks: BackgroundTasks, fid: str, seq: str, hd: str):
    """
    v3 版中读取数据库ts视频发送给客户端
    :param background_tasks:
    :param fid:
    :param seq:
    :param hd:
    :return:
    """
    if defaultdb == "":
        return Response404(data="此功能禁用，请先连接数据库")
    if not (fid in idata):
        return Response404(data="NOT FOUND " + fid)
    vname = fid + str(seq) + ".ts"
    if "4gtv-live" in fid:
        host = "https://" + host2
    else:
        host = "https://" + host1
    gap, seq, url, begin = get.generalfun(fid, hd)
    if downchoose == "online":
        background_tasks.add_task(backtaskonline, url, fid, seq, hd, begin, host)
    elif downchoose == "local":
        background_tasks.add_task(backtasklocal, url, fid, seq, hd, begin, host)
    for i in range(1, 10):
        if get.filename.get(vname) and get.filename.get(vname) != 0:
            sql = "SELECT vcontent FROM video where vname='{}'".format(vname)
            content = DBconnect.fetchone(sql)
            return Response(content=content['vcontent'], status_code=200, headers=headers, media_type='video/MP2T')
        else:
            await asyncio.sleep(2 - i * 0.095)
    return Response404()


@app.get('/channel.m3u8')
async def channel(
        host: Any = Query(localhost),
        fid: Any = Query(...),
        hd: Any = Query("720")):
    """
    新版优化api v2
    在redis中设置截止时间，过期重新获取保存到redis，默认通过读取redis参数，构造ts链接，待优化redis无参数请求耗时较长
    有些缺陷即 该版本不具有视频缓冲区，他可以极大减少通信耗时，该版本没有
    :param host:
    :param fid:
    :param hd:
    :return:
    """
    if not (fid in idata):
        return Response404(data=f"Not found {fid}")
    t = idata[fid].get("lt", 0) - now_time()
    if t > 0:
        return Response404(data=f"{fid} 频道暂不可用，请过 {t} 秒后再试")
    return StreamingResponse(get.generatem3u8(host, fid, hd), 200, {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Content-Type': 'application/vnd.apple.mpegurl',
    })


@app.get('/channel2.m3u8')
async def channel2(
        fid: Any = Query(...),
        hd: Any = Query("720")):
    """
    读取redis获取链接进行重定向，没有就请求url后保存到redis
    :param fid:
    :param hd:
    :return:
    """
    if not (fid in idata):
        return Response404(data=f"Not found {fid}")
    t = idata[fid].get("lt", 0) - now_time()
    if t > 0:
        return Response404(data=f"{fid} 频道暂不可用，请过 {t} 秒后再试")
    return RedirectResponse(get.geturl(fid, hd), status_code=302)


@app.get('/channel3.m3u8', summary="转发m3u8")
async def channel3(
        host: Any = Query(localhost),
        fid: Any = Query(...),
        hd: Any = Query("720")):
    """
    新版优化api v3
    在redis中设置截止时间，过期重新获取保存到redis，默认通过读取redis参数，构造ts链接，待优化redis无参数请求耗时较长
    对api请求进一步优化
    :param host:
    :param fid:
    :param hd:
    :return:
    """
    if not (fid in idata):
        return Response404(data=f"Not found {fid}")
    t = idata[fid].get("lt", 0) - now_time()
    if t > 0:
        return Response404(data=f"{fid} 频道暂不可用，请过 {t} 秒后再试")
    if not host:
        if "4gtv-live" not in fid:
            host = "https://" + host1
        else:
            return Response200(data="参数无效")
    return StreamingResponse(get.generatem3u8(host, fid, hd), 200, {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Content-Type': 'application/vnd.apple.mpegurl',
        'Expires': '-1',
    })


@app.get('/program.m3u')
async def program(host: Any = Query(None),
                  hd: Any = Query("720"),
                  name="channel"):
    """
    生成频道表
    :param name:
    :param host:
    :param hd:
    :return:
    """
    return StreamingResponse(generate_m3u(host, hd, name), 200, {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Content-Type': 'application/vnd.apple.mpegurl',
        'Expires': '-1',
    })


@app.get('/EPG.xml')
async def epg(background_tasks: BackgroundTasks):
    """
    获取4gtv中未来3天所有节目表
    :param background_tasks:
    :return:
    """
    pathname = PATH / "assets/EPG.xml"
    if pathname.exists() and time.strftime('%Y-%m-%d') == time.strftime('%Y-%m-%d',
                                                                        time.localtime(pathname.lstat().st_ctime)):
        with open(pathname, "r", encoding="utf-8") as f:
            data = f.read()
            f.close()
    else:
        with request.get("https://agit.ai/239144498/demo/raw/branch/master/4gtvchannel.xml") as res:
            data = res.content
            if res.status_code == 200:
                background_tasks.add_task(writefile, pathname, data)
    return Response(data, 200, media_type='application/xml')


@app.get("/live/{file_path:path}")
async def downlive(file_path: str, token1: str = None, expires1: int = None):
    """
    v2 版下载中转
    :param file_path:
    :param token1:
    :param expires1:
    :return:
    """
    file_path = "/live/" + file_path
    if "live/pool/" not in file_path:
        return Response404(data="error")
    if token1 and expires1:
        file_path += f"?token1={token1}&expires1={expires1}"
    if "live/pool/4gtv-live" in file_path:
        url = "https://" + host2 + file_path
    else:
        url = "https://" + host1 + file_path
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    with request.get(url=url, headers=header) as res:
        if res.status_code != 200:
            return Response404(status_code=403)
        return Response(content=res.content, status_code=200, headers=headers, media_type='video/MP2T')


if __name__ == '__main__':
    import uvicorn

    print(localhost)
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")  # reload=True, debug=True
