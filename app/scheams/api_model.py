# -*- coding: utf-8 -*-
# @Time    : 2022/10/22
# @Author  : Naihe
# @Email   : 239144498@qq.com
# @File    : api_model.py
# @Software: PyCharm
from enum import Enum


class Clarity(str, Enum):
    f = "360"  # 流畅 360P
    s = "480"  # 标准 480P
    c = "720"  # 高清 720P
    h = "1080"  # 超清 1080P


class Channels(str, Enum):
    online = "online"
    channel = "channel"
    channel2 = "channel2"
    channel3 = "channel3"
