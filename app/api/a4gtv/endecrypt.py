#!/usr/bin python3
# -*- coding: utf-8 -*-
import asyncio
import re
import json
from urllib.parse import urljoin

from app.api.a4gtv.tools import get_4gtv, now_time
from app.common.header import random_header
from app.common.request import request
from app.conf.config import data3, edata


def decrypt(info):
    true = None
    false = None
    null = None
    with request.post(url=data3['a3'], json={"Data": info["Data"]}) as res:
        info = eval(json.loads(res.content.decode("utf-8")))
        link = info["flstURLs"].pop()
        return link


def encrypt(fs4GTV_ID):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": random_header()
    }
    url = data3['a2']
    value = edata[fs4GTV_ID]
    data = {'value': value}
    with request.post(url=url, json=data, headers=headers) as res:
        return res.json()


def get4gtvurl(fs4GTV_ID):
    start = now_time()
    if "http" in data3['a3']:
        info = encrypt(fs4GTV_ID)
        link = decrypt(info)
        url = re.sub(r"(\w+\.m3u8)", "stream1.m3u8", link)
        data = get_4gtv(url)
        return 200, url, data, start
    if "http" in data3['a1']:
        url = urljoin(data3['a1'], "?fid={}&type=v3".format(fs4GTV_ID))
        header = {
            "Accept": "*/*",
            "User-Agent": random_header(),
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        }
        with request.get(url=url, headers=header) as res:
            data = res.text
            return res.status_code, res.url.__str__(), data, start


if __name__ == '__main__':
    a = get4gtvurl("4gtv-4gtv018")
    print(a)
