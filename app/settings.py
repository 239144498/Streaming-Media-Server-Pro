#!/usr/bin python3
# -*- coding: utf-8 -*-
import os
import requests

from configparser import ConfigParser
from pathlib import Path
from loguru import logger


request = requests.session()
logger.info("配置加载中...")


PATH = Path(__file__).parent
ROOT = PATH.parent

cfg = ConfigParser()
cfg.read(ROOT / "app/assets/config.ini", encoding="utf-8")
redis_cfg = dict(cfg.items("redis"))
mysql_cfg = dict(cfg.items("mysql"))
postgre_cfg = dict(cfg.items("postgresql"))
default_cfg = dict(cfg.items("default"))
other_cfg = dict(cfg.items("other"))

PORT = int(os.getenv("PORT", default=default_cfg.get("port")))

host1 = default_cfg.get("host1")
host2 = default_cfg.get("host2")
vbuffer = int(default_cfg.get("vbuffer"))
downurls = eval(default_cfg.get("downurls"))
downurls = downurls * (vbuffer//len(downurls)+1)
localhost = os.environ.get("localhost") or default_cfg.get("localhost")

xmlowner = other_cfg.get("xmlowner")
xmlrepo = other_cfg.get("xmlrepo")
xmlaccess_token = other_cfg.get("xmlaccess_token")
repoowner = other_cfg.get("repoowner")
repoaccess_token = other_cfg.get("repoaccess_token")
key = other_cfg.get("key", "").encode()
iv = other_cfg.get("iv", "").encode()

if xmlowner and xmlrepo and xmlaccess_token:
    xmlState = True
else:
    xmlState = False
if repoowner and repoaccess_token:
    repoState = True
else:
    repoState = False

headers = {
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
}


idata = eval(request.get("https://agit.ai/239144498/owner/raw/branch/master/data",
                          headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"}).content)
data3 = eval(request.get("https://agit.ai/239144498/owner/raw/branch/master/data3",
                          headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"}).content)
gdata = eval(request.get("https://agit.ai/239144498/owner/raw/branch/master/data2",
                          headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"}).content)
HD = {
    "360": "stream0.m3u8", "480": "stream1.m3u8", "720": "stream2.m3u8", "1080": "stream2.m3u8",
}
logger.info("配置加载完成")