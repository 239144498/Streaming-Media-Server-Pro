#!/usr/bin python3
# -*- coding: utf-8 -*-
import time
from typing import Any
from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi import FastAPI, Query, Response, BackgroundTasks
from aiohttp import ClientSession

from app.utile import *

app = FastAPI()


@app.get('/')
def abc():
    return Response(status_code=403, content="no access")


@app.get('/online.m3u8')
def generate_file6(
        background_tasks: BackgroundTasks,
        host: Any = Query(None),
        fid: Any = Query(...),
        hd: Any = Query("1080")):
    """
    最新版 apiv3
    该版本具有redis缓存，视频中转缓存处理等优点
    :param background_tasks:
    :param host:
    :param fid:
    :param hd:
    :return:
    """
    if not host:
        if "4gtv-live" in fid:
            host = "https://xxxx"
        else:
            host = os.environ['host']
    return StreamingResponse(get.new_generatem3u8(host, fid, hd, background_tasks), 200, {
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        'Content-Type': 'application/vnd.apple.mpegurl',
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Credentials": "true",
        "Expires": "-1",
    })


@app.get('/call.ts')
def call(background_tasks: BackgroundTasks, fid: str, seq: str, hd: str):
    p = fid + str(seq) + ".ts"
    if "4gtv-live" in fid:
        host = "https://xxxx"
    else:
        host = os.environ['host']
    gap, seq, url, begin = get.generalfun(fid, hd)
    background_tasks.add_task(backtaskonline, url, fid, seq, hd, begin, host)
    for i in range(1, 10):
        if get.filename.get(p) and get.filename.get(p) != 0:
            sql = "SELECT vcontent FROM video where vname='{}'".format(p)
            content = mysql.fetchone(sql)
            return Response(content=content['vcontent'], status_code=200, headers={
                'Content-Type': 'video/MP2T',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=600',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Headers": "content-type, date",
                "Access-Control-Allow-Methods": "GET",
                "Age": "0",
                'Accept-Ranges': 'bytes',
                'Content-Length': str(len(content['vcontent'])),
            }, media_type='video/MP2T')
        else:
            time.sleep(1.2 - i * 0.095)
    else:
        print("未命中", fid)
        p = fid + str(seq - 1) + ".ts" + hd
        if get.filename.get(p) and get.filename.get(p) != 0:
            sql = "SELECT vcontent FROM video where vname='{}'".format(p)
            content = mysql.fetchone(sql)
            return Response(content=content.get("vcontent"), status_code=200, headers={
                'Content-Type': 'video/MP2T',
                'Connection': 'keep-alive',
                'Cache-Control': 'max-age=600',
                'Access-Control-Allow-Origin': '*',
                "Access-Control-Allow-Headers": "content-type, date",
                "Access-Control-Allow-Methods": "GET",
                "Age": "0",
                'Accept-Ranges': 'bytes',
                'Content-Length': str(len(content['vcontent'])),
            }, media_type='video/MP2T')


@app.get('/channel.m3u8')
def generate_file1(
        host: Any = Query(os.environ["local"]),
        fid: Any = Query(...),
        hd: Any = Query("720")):
    """
    新版优化apiv2
    在redis中设置截止时间，过期重新获取保存到redis，默认通过读取redis参数，构造ts链接，待优化redis无参数请求耗时较长
    最大缺陷即 代理中转需要缓冲区，以减少下载视频耗时，该版本没有
    :param host:
    :param fid:
    :param hd:
    :return:
    """
    return StreamingResponse(get.generatem3u8(host, fid, hd), 200, {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Content-Type': 'application/vnd.apple.mpegurl',
        'Expires': '-1',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Credentials': 'true',
    })


@app.get('/channel2.m3u8')
def generate_file2(
        fid: Any = Query(...),
        hd: Any = Query("720")):
    """
    读取redis获取链接进行重定向，没有就请求url后保存到redis
    :param fid:
    :param hd:
    :return:
    """
    return RedirectResponse(get.geturl(fid, hd))


@app.get('/program.m3u')
def generate_file3(host: Any = Query(os.environ['local']),
                   hd: Any = Query("720"),
                   name="online"):
    """
    生成节目单
    :param name:
    :param host:
    :param hd:
    :return:
    """
    name += ".m3u8"
    return StreamingResponse(generate_m3u(host, hd, name), 200, {
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Content-Type': 'application/vnd.apple.mpegurl',
        'Expires': '-1',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
        'Access-Control-Allow-Credentials': 'true',
    })


@app.get('/EPG.xml')
def test(background_tasks: BackgroundTasks):
    if os.path.exists("EPG.xml"):
        with open("EPG.xml", "r", encoding="utf-8") as f:
            data = f.read()
            f.close()
    else:
        with request.get("https://xxx/239144498/demo/raw/branch/master/4gtvchannel.xml") as res:
            data = res.content
            if res.status_code == 200:
                background_tasks.add_task(writefile, "EPG.xml", data)
    return Response(data, 200)


@app.get("/live/{file_path:path}")
async def download(file_path: str, token: str = None, expires: int = None, token1: str = None, expires1: int = None):
    file_path = "/live/" + file_path
    if "live/pool/" not in file_path:
        return Response(status_code=404, content="404")
    if token and expires:
        file_path += f"?token={token}&expires={expires}"
    if token1 and expires1:
        file_path += f"?token1={token1}&expires1={expires1}"
    if "live/pool/4gtv-live" in file_path:
        url = "https://xxxx" + file_path
        host = "xxx"  # api请求
    else:
        host = "xxx"
        url = os.environ['host'] + file_path
    header = {
        'Host': host,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    async with ClientSession(headers=header) as request:
        async with request.get(url=url, headers=header) as res:
            if res.status != 200:
                return Response(status_code=403)
            return Response(content=await res.content.read(), status_code=200, headers=headers, media_type='video/MP2T')

@app.get("/down/{url:path}")
def down(url):
    a = time.time()
    sql = "SELECT vcontent FROM video where vname='{}'".format(url)
    content = mysql.fetchone(sql)
    b = time.time()
    print(b - a)
    return Response(content['vcontent'], status_code=200, headers={
        'Content-Type': 'video/MP2T',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=600',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'content-type, date',
        'Access-Control-Allow-Methods': 'GET',
        'Age': '0',
        'Via': 'ViaMotion Edge',
        'X-Anevia-Edge': 'MISS',
        'X-Cache': 'MISS, HIT',
        'Accept-Ranges': 'bytes'
    }, media_type='video/MP2T')


# alter table video engine = InnoDB
if __name__ == '__main__':
    import uvicorn

    print(os.environ['local'])
    # uvicorn.run(app='app.main:app', host="127.0.0.1", port=15000, reload=True, debug=True)
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
