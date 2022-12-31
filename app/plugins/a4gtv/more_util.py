# -*- coding: utf-8 -*-
# @Time    : 2022/10/30
# @Author  : Naihe
# @Email   : 239144498@qq.com
# @File    : more_util.py
# @Software: PyCharm
import re
from base64 import b64encode
from urllib.parse import urlencode, unquote, quote_plus, urlparse, parse_qsl, urlunparse, urljoin
from app.conf import config


def is_url(url):
    regex = re.compile(config.url_regex)
    if regex.match(url):
        return True
    else:
        return False


def parse(url):
    url = urlencode(url).replace("url=", "")
    url = unquote(url)
    return url


def processing(url, data):
    for _temp in data:
        if ".ts" in _temp:
            if is_url(_temp):
                yield "/pdl?url=" + b64encode(_temp.encode("utf-8")).decode("utf-8")
            else:
                yield "/pdl/?url=" + b64encode(urljoin(url, _temp).encode("utf-8")).decode("utf-8")
        else:
            yield _temp
        yield "\n"


def splicing(url, query_params):
    url_parsed = list(urlparse(url))
    temp_para = parse_qsl(url_parsed[4])
    temp_para.extend(parse_qsl(query_params.__str__()))
    url_parsed[4] = urlencode(temp_para)
    url_new = urlunparse(url_parsed)
    return url_new

