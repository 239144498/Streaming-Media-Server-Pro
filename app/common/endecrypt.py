#!/usr/bin python3
# -*- coding: utf-8 -*-
import re
import json

from base64 import b64decode, b64encode
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES

from app.modules.request import request
from app.settings import key, iv, HD, data3


def decrypt(info):
    ciphertext = b64decode(info["Data"])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    info = json.loads(plaintext.decode('utf-8'))
    link = info["flstURLs"][1]
    return link


def encrypt(fs4GTV_ID, fnID):
    raw = {"fnCHANNEL_ID": fnID, "fsASSET_ID": fs4GTV_ID, "fsDEVICE_TYPE": "pc",
           "clsIDENTITY_VALIDATE_ARUS": {"fsVALUE": ""}}
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = bytes(json.dumps(raw), 'utf-8')
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    value = b64encode(ciphertext).decode('utf-8')
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
    }
    # 需要特定地区ip才能访问
    url = data3['a2']
    data = {'value': value}
    with request.post(url=url, json=data, headers=headers) as res:
        return res.json()


def get4gtvurl(fs4GTV_ID, fnID, hd):
    if key and iv:  # 需要特定地区ip请求接口会报错
        info = encrypt(fs4GTV_ID, fnID)
        link = decrypt(info)
    else:
        url = data3['a1'] + "?vid={}&nid={}&fid={}".format(fs4GTV_ID, fnID, fs4GTV_ID)
        res = request.get(url=url)
        link = res.url
    return re.sub(r"(\w+\.m3u8)", HD[str(hd)], link)


if __name__ == '__main__':
    a = get4gtvurl("4gtv-4gtv018", 11, 720)
    print(a)
