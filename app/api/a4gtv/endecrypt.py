#!/usr/bin python3
# -*- coding: utf-8 -*-
import asyncio
import re
import json
from urllib.parse import urljoin

import aiohttp

from app.api.a4gtv.tools import get_4gtv, now_time
from app.common.header import random_header
from app.conf.config import data3, edata


async def decrypt(info):
    true = None
    false = None
    null = None
    async with aiohttp.ClientSession() as session:
        async with session.post(url=data3['a3'], json={"Data": info["Data"]}) as res:
            info = eval(json.loads(await res.text(encoding="utf-8")))
            link = info["flstURLs"].pop()
            return link


async def encrypt(fs4GTV_ID):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": random_header()
    }
    url = data3['a2']
    value = edata[fs4GTV_ID]
    data = {'value': value}
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, json=data, headers=headers) as res:
            return await res.json()


async def get4gtvurl(fs4GTV_ID):
    if "http" in data3['a3']:
        info = await encrypt(fs4GTV_ID)
        link = await decrypt(info)
        url = re.sub(r"(\w+\.m3u8)", "stream1.m3u8", link)
        data, start = await get_4gtv(url)
        return 200, url, data, start
    if "http" in data3['a1']:
        url = urljoin(data3['a1'], "?fid={}&type=v2".format(fs4GTV_ID))
        header = {
            "Accept": "*/*",
            "User-Agent": random_header(),
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        }
        start = now_time()
        async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=header, allow_redirects=True) as res:
                data = await res.text()
                return res.status, res.url.__str__(), data, start


if __name__ == '__main__':
    a = asyncio.run(get4gtvurl("4gtv-4gtv018"))
    print(a)

