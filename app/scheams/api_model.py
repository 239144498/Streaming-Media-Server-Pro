# -*- coding: utf-8 -*-
# @Time    : 2022/10/22
# @Author  : Naihe
# @Email   : 239144498@qq.com
# @File    : api_model.py
# @Software: PyCharm
from enum import Enum


class Clarity(str, Enum):
    f = "360"
    s = "480"
    c = "720"
    h = "1080"


class Channels(str, Enum):
    online = "online"
    channel = "channel"
    channel2 = "channel2"
    channel3 = "channel3"


class Witch(str, Enum):
    yes = "y"
    no = "n"
