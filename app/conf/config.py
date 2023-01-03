import hashlib
import time
import uuid
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

from pydantic import BaseSettings
import os

import requests
from loguru import logger
from configparser import ConfigParser
from platform import platform, python_version, machine


class Config(BaseSettings):
    TITLE: Optional[str] = "Streaming Media Server Pro"

    DESC: Optional[str] = """
### **程序主要功能：**
- 高效流媒体（具有缓冲区）
- 代理任意视频网站的视频流
- 生成m3u文件
- 生成m3u8文件
- 异步下载流
- 流媒体转发
- 生成[EPG节目单](https://agit.ai/239144498/demo/raw/branch/master/4gtvchannel.xml) 每日实时更新
- 分布式处理ts片
- Redis缓存参数
- MySql缓存数据
- 正向代理请求
- 自定义节目频道
- 自定义电视台标
- 自定义清晰度
- 支持反向代理或CDN（负载均衡）
### 使用说明
1. 接口说明: [查看接口使用教程](https://www.cnblogs.com/1314h/p/16651157.html)
2. 项目代码: [Github开源代码](https://github.com/239144498/Streaming-Media-Server-Pro)
### 接口列表：
- **向下滑动查看**
"""

    VERSION = "2.6"

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

    datadir = ROOT / 'vtemp'

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
mdata = hashlib.md5(config.VERSION.encode()).hexdigest()
vbuffer = int(default_cfg.get("vbuffer"))
downurls = eval(default_cfg.get("downurls"))
downurls = downurls * (vbuffer // len(downurls) + 1)
localhost = os.environ.get("localhost") or default_cfg.get("localhost")
defaultdb = default_cfg.get("defaultdb")
purl = os.getenv("purl")
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
mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
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
machine = f"Pyhton/{python_version()} ({machine()} {platform()} {mac}) Version/{config.VERSION}"
print(".", end="")
data3 = None
try:
    tx = int(time.time() - int(request.get(urljoin(data3["a1"], "sync"), headers={"User-Agent": machine}).json()["data"]))
except Exception as e:
    tx = 0
print(".", end="")

gdata = None
print(".", end="")
version = None
print(".", end="\n")
if config.VERSION != str(version):
    logger.warning(f"当前版本为{config.VERSION}，最新版本为{version}，请及时更新！")
    logger.warning("更新地址：https://github.com/239144498/Streaming-Media-Server-Pro")

if localhost and "http" not in localhost:
    logger.warning("localhost配置错误，具体查看教程https://www.cnblogs.com/1314h/p/16651157.html")

logger.info("配置加载完成")
