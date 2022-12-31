#!/usr/bin python3
# -*- coding: utf-8 -*-
import base64
import hashlib
from urllib.parse import urljoin

from loguru import logger

from app.plugins.a4gtv.tools import now_time
from app.common.request import request
from app.conf.config import data3, machine, config, mdata, tx


def get4gtvurl(fsid):
    _a = now_time()
    url = urljoin(data3['a1'], "?type=v5".format(fsid))
    data = {"t": _a - tx, "fid": fsid, "v": config.VERSION}
    header = {
        "Accept": "*/*",
        "User-Agent": machine,
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "v": hashlib.md5(bytes(str(data) + mdata, 'utf8')).hexdigest(),
    }
    with request.post(url=url, headers=header, data=data, allow_redirects=True) as res:
        logger.success(f"{fsid} {res.status_code}")
        try:
            data = res.json()["data"]
            msg = res.json()["msg"]
            return res.status_code, data["url"], data['data'], _a, msg
        except:
            return res.status_code, None, res.text, _a, ""


if __name__ == '__main__':
    a = get4gtvurl("4gtv-4gtv018")
    print(a)
