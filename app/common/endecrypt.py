#!/usr/bin python3
# -*- coding: utf-8 -*-
# @Author: Naihe
# @Email: 239144498@qq.com
# @Software: Streaming-Media-Server-Pro
import re
import json

from base64 import b64decode, b64encode

import requests
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

from app.modules.request import request
from app.settings import key, iv, HD, data3, edata


def decrypt(info):
    ciphertext = b64decode(info["Data"])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    info = json.loads(plaintext.decode('utf-8'))
    link = info["flstURLs"][1]
    return link


def encrypt(fs4GTV_ID, fnID):
    value = edata[fs4GTV_ID]
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
    }
    # 需要特定地区ip才能访问，否则请求失败
    url = data3['a2']
    data = {'value': value}
    with request.post(url=url, json=data, headers=headers) as res:
        return res.json()


def decrypt2(info):
    true = True
    false =False
    null = None
    with requests.post(url=data3['a3'], json={"Data": info["Data"]}) as res:
        info = eval(json.loads(res.content.decode("utf-8")))
        link = info["flstURLs"][1]
        return link


def encrypt2(fs4GTV_ID, fnID):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
    }
    url = data3['a2']
    value = edata[fs4GTV_ID]
    data = {'value': value}
    with request.post(url=url, json=data, headers=headers) as res:
        return res.json()


def get4gtvurl(fs4GTV_ID, fnID, hd):
    if key and iv:  # 需要特定地区ip请求接口会报错
        info = encrypt(fs4GTV_ID, fnID)
        link = decrypt(info)
    elif "http" in data3['a3']:
        info = encrypt2(fs4GTV_ID, fnID)
        link = decrypt2(info)
    elif "http" in data3['a1']:
        url = data3['a1'] + "?vid={}&nid={}&fid={}".format(fs4GTV_ID, fnID, fs4GTV_ID)
        with request.get(url=url) as res:
            if res.status_code != 200 and 310 - res.status_code > 10:
                res.encoding = "utf-8"
                print(res.text)
            link = res.url
        return link
    else:
        raise Exception("未找到链接")
    return re.sub(r"(\w+\.m3u8)", HD[str(hd)], link)


if __name__ == '__main__':
    a = get4gtvurl("4gtv-4gtv018", 11, 720)
    print(a)

