#!/usr/bin python3
# -*- coding: utf-8 -*-
# @Author: Naihe
# @Email: 239144498@qq.com
# @Software: Streaming-Media-Server-Pro
import re
import json
import requests

from app.common.tools import get_4gtv
from app.settings import HD, data3, edata


def decrypt(info):
    true = None
    false = None
    null = None
    with requests.post(url=data3['a3'], json={"Data": info["Data"]}) as res:
        info = eval(json.loads(res.content.decode("utf-8")))
        link = info["flstURLs"].pop()
        return link


def encrypt(fs4GTV_ID):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
    }
    url = data3['a2']
    value = edata[fs4GTV_ID]
    data = {'value': value}
    with requests.post(url=url, json=data, headers=headers) as res:
        return res.json()


def get4gtvurl(fs4GTV_ID, hd):
    if "http" in data3['a3']:
        info = encrypt(fs4GTV_ID)
        link = decrypt(info)
        url = re.sub(r"(\w+\.m3u8)", HD[str(hd)], link)
        status_code, data = get_4gtv(url)
        return status_code, url, data
    if "http" in data3['a1']:
        url = data3['a1'] + "?fid={}&type=1".format(fs4GTV_ID)
        header = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        }
        with requests.get(url=url, headers=header) as res:
            return res.status_code, res.url, res.text


if __name__ == '__main__':
    a = get4gtvurl("4gtv-4gtv018", 720)
    print(a)

