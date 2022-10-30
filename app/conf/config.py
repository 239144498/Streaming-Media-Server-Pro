from pathlib import Path
from typing import Optional
from pydantic import BaseSettings
import os

import requests
from loguru import logger
from configparser import ConfigParser


class Config(BaseSettings):
    TITLE: Optional[str] = "Streaming Media Server Pro"

    DESC: Optional[str] = """
### **程序主要功能：**
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

    VERSION = "2.4"

    CONTACT = {
        "name": "Naihe",
        "url": "https://github.com/239144498/",
        "email": "239144498@qq.com",
    }

    ORIGINS = [
        "*"
    ]

    ROOT = Path(__file__).parent.parent  # .app

    LOG_DIR = ROOT / "log"

    count = 0

    url_regex = r"(http|https)://((?:[\w-]+\.)+[a-z0-9]+)((?:\/[^/?#]*)+)?(\?[^#]+)?(#.+)?"


logger.info("配置加载中...")
config = Config()

request = requests.session()

cfg = ConfigParser()
cfg.read(config.ROOT / "assets/config.ini", encoding="utf-8")
redis_cfg = dict(cfg.items("redis"))
mysql_cfg = dict(cfg.items("mysql"))
default_cfg = dict(cfg.items("default"))
advanced_cfg = dict(cfg.items("advanced"))
other_cfg = dict(cfg.items("other"))
PORT = int(os.getenv("PORT", default=default_cfg.get("port")))

vbuffer = int(default_cfg.get("vbuffer"))
downurls = eval(default_cfg.get("downurls"))
downurls = downurls * (vbuffer // len(downurls) + 1)
localhost = os.environ.get("localhost") or default_cfg.get("localhost")
defaultdb = default_cfg.get("defaultdb")

host1 = advanced_cfg.get("host1")
host2 = advanced_cfg.get("host2")
tvglogo = advanced_cfg.get("tvglogo")
proxies = advanced_cfg.get("proxies")
DEBUG = eval(os.getenv("DEBUG", default=advanced_cfg.get("debug", "False")))
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
    'Cache-Control': 'max-age=600',
    'Accept-Ranges': 'bytes'
}
headers2 = {
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Content-Type': 'application/vnd.apple.mpegurl',
    'Expires': '-1',
}
print(".", end="")
idata = eval(request.get("https://raw.githubusercontent.com/382420058/owner/main/data",
                         headers={
                             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"}).content)
print(".", end="")
data3 = eval(request.get("https://raw.githubusercontent.com/382420058/owner/main/data3",
                         headers={
                             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"}).content)
print(".", end="")
gdata = eval(request.get("https://raw.githubusercontent.com/382420058/owner/main/data2",
                         headers={
                             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"}).content)
print(".", end="")
edata = eval(request.get("https://raw.githubusercontent.com/382420058/owner/main/data4",
                         headers={
                             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"}).content)
print(".", end="")
version = eval(request.get("https://raw.githubusercontent.com/382420058/owner/main/version",
                           headers={
                               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0"}).text)

print(".", end="\n")
if config.VERSION != str(version):
    logger.warning(f"当前版本为{config.VERSION}，最新版本为{version}，请及时更新！")
    logger.warning("更新地址：https://github.com/239144498/Streaming-Media-Server-Pro")

HD = {
    "360": "stream0.m3u8", "480": "stream1.m3u8", "720": "stream2.m3u8", "1080": "stream2.m3u8",
}

logger.info("配置加载完成")
