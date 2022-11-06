#!/usr/bin python3
# -*- coding: utf-8 -*-
# @Author: Naihe
# @Email: 239144498@qq.com
# @Software: Streaming-Media-Server-Pro
import os
import requests

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
        return self.request.post(url, data=data, json=json, headers=headers, proxies=self.proxies, timeout=10, **kwargs)

    def put(self, url, data=None, json=None, headers=None, **kwargs):
        return self.request.put(url, data=data, json=json, headers=headers, proxies=self.proxies, **kwargs)

    def delete(self, url, data=None, json=None, headers=None, **kwargs):
        return self.request.delete(url, data=data, json=json, headers=headers, proxies=self.proxies, **kwargs)


request = netreq()


if __name__ == '__main__':
    url = "https://httpbin.org/anything"
    data = {
        "1": "2"
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
    }
    # with request.post(url=url, json=data, headers=headers) as res:
    with request.get(url=url, headers=headers) as res:
        print(res.text)
        print(res.status_code)
