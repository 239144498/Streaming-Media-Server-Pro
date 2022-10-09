#!/usr/bin python3
# -*- coding: utf-8 -*-
# @Author: Naihe
# @Email: 239144498@qq.com
# @Software: Streaming-Media-Server-Pro
import os

from configparser import ConfigParser
from pathlib import Path
from loguru import logger

from app.modules.request import request

logger.info("配置加载中...")


PATH = Path(__file__).parent
ROOT = PATH.parent

cfg = ConfigParser()
cfg.read(ROOT / "app/assets/config.ini", encoding="utf-8")
try:
    redis_cfg = dict(cfg.items("redis"))
    mysql_cfg = dict(cfg.items("mysql"))
    postgre_cfg = dict(cfg.items("postgresql"))
    default_cfg = dict(cfg.items("default"))
    advanced_cfg = dict(cfg.items("advanced"))
    other_cfg = dict(cfg.items("other"))
except Exception as e:
    logger.error(e)
    raise Exception("检查config.ini是否配置正确！教程地址：https://www.cnblogs.com/1314h/p/16651157.html")

PORT = int(os.getenv("PORT", default=default_cfg.get("port")))
localhost = os.environ.get("localhost") or default_cfg.get("localhost")
downchoose = default_cfg.get("downchoose")
defaultdb = default_cfg.get("defaultdb")
vbuffer = int(default_cfg.get("vbuffer"))
downurls = eval(default_cfg.get("downurls"))
downurls = downurls * (vbuffer//len(downurls)+1)

host1 = advanced_cfg.get("host1")
host2 = advanced_cfg.get("host2")
tvglogo = advanced_cfg.get("tvglogo")
proxies = advanced_cfg.get("proxies")
if proxies:
    os.environ["proxies"] = proxies

xmlowner = other_cfg.get("xmlowner")
xmlrepo = other_cfg.get("xmlrepo")
xmlaccess_token = other_cfg.get("xmlaccess_token")
repoowner = other_cfg.get("repoowner")
repoaccess_token = other_cfg.get("repoaccess_token")

if xmlowner and xmlaccess_token:
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
    'Accept-Ranges': 'bytes'
}


idata = eval(request.get("https://agit.ai/239144498/owner/raw/branch/master/data",
                          headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"}).content)
data3 = eval(request.get("https://agit.ai/239144498/owner/raw/branch/master/data3",
                          headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"}).content)
gdata = eval(request.get("https://agit.ai/239144498/owner/raw/branch/master/data2",
                          headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"}).content)
edata = eval(request.get("https://agit.ai/239144498/owner/raw/branch/master/data4",
                          headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"}).content)
HD = {
    "360": "stream0.m3u8", "480": "stream1.m3u8", "720": "stream2.m3u8", "1080": "stream2.m3u8",
}

describe = """\n
主要实现功能：
- 生成m3u文件
- 生成m3u8文件
- 视频中转（具有缓冲区）
- 异步下载视频
- 流媒体转发
- 生成[EPG节目单](https://agit.ai/239144498/demo/raw/branch/master/4gtvchannel.xml) 每日实时更新
- 分布式处理ts片段
- Redis缓存参数
- MySql或PostgreSql缓存视频
- 正向代理请求
- 自定义增加节目频道
- 自定义电视台标
- 清晰度可自定义
- 反向代理或套CDN请求（负载均衡）
### 使用说明
1. 接口说明: [查看接口使用教程](https://www.cnblogs.com/1314h/p/16651157.html)
2. 项目代码: [Github开源代码](https://github.com/239144498/Streaming-Media-Server-Pro)
### 接口列表：
- **向下滑动查看**
"""

logger.info("配置加载完成")
