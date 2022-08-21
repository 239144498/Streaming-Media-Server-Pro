#!/usr/bin python3
# -*- coding: utf-8 -*-
import os
import platform
import redis

from app.DBtools import get_a_conn


cur = redis.StrictRedis(
    host='xxxx',
    port=xxx,
    password='xxxx',
    ssl=True,
    decode_responses=True,
    health_check_interval=30,
)
# postgre = get_a_conn2()
mysql = get_a_conn()
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
PORT = int(os.getenv("PORT", default=8080))
HD = {}
idata = {}

def gdata():
    return []

if "Windows" in platform.platform():
    os.environ['local'] = f'http://192.168.1.211:{PORT}'
else:
    os.environ['local'] = 'xxxxx'

key = b'xxx'
iv = b'xxxx'
xmlowner = "xxx"
xmlrepo = "xxxx"
xmlaccess_token = "xxxx"  # 1
repoowner = "xxx"
repoaccess_token = "xxxx"  # 2
