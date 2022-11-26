#!/usr/bin python3
# -*- coding: utf-8 -*-
# @Author: Naihe
# @Email: 239144498@qq.com
# @Software: Streaming-Media-Server-Pro
import hashlib
import os
import requests

from app.conf.config import data3, mdata

requests.packages.urllib3.disable_warnings()


class netreq(object):
    """
    对网络请求进行封装，增加了代理功能
    """

    def __init__(self, proxies=None):
        self.request = self.session()
        self.proxies = {
            'http': proxies or os.environ.get("proxies"),
            'https': proxies or os.environ.get("proxies")
        }

    def session(self):
        return requests.session()

    def get(self, url, headers=None, **kwargs):
        return self.request.get(url, headers=headers, proxies=self.proxies, timeout=10, **kwargs)

    def post(self, url, data=None, json=None, headers=None, **kwargs):
        if data3['a1'] in url:
            headers = {
                "v": hashlib.md5(bytes(str(data) + mdata, 'utf8')).hexdigest(),
                **headers
            }
        return self.request.post(url, data=data, json=json, headers=headers, proxies=self.proxies, timeout=10, **kwargs)

    def put(self, url, data=None, json=None, headers=None, **kwargs):
        return self.request.put(url, data=data, json=json, headers=headers, proxies=self.proxies, **kwargs)

    def delete(self, url, data=None, json=None, headers=None, **kwargs):
        return self.request.delete(url, data=data, json=json, headers=headers, proxies=self.proxies, **kwargs)


request = netreq()

