# -*- coding: utf-8 -*-
# @Time    : 2022/10/30
# @Author  : Naihe
# @Email   : 239144498@qq.com
# @File    : more_util.py
# @Software: PyCharm
import re
import time
import requests
from base64 import b64encode
from urllib.parse import urlencode, unquote, quote_plus, urlparse, parse_qsl, urlunparse, urljoin, parse_qs
from app.conf import config
from loguru import logger
from app.conf.config import ytb_stream

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
        # 补充/proxy接口，如果获取的是不含域名的m3u8列表，则拼出完整地址        
        elif len(_temp)>4:
            if _temp[0] != '#' and _temp[:4] != 'http':
                yield "/proxy?url=" + urljoin(url, _temp)
            else:
                yield _temp
        else:
            yield _temp
        yield "\n"

def update_ytb(url,headers,stream_id):
    response = requests.get(url, headers=headers).text
    pattern = re.search(r'hlsManifestUrl.+?(https://.+?m3u8)',response)
    stream_url = pattern.group(1)
    pattern2 = re.search(r'expire/(\d{10})',stream_url)
    expire = int(pattern2.group(1))    
    ytb_stream[stream_id] = {"expire":expire,"url":url,"stream_url":stream_url}
    logger.success(f"youtube直播源已更新 {ytb_stream[stream_id]}")
    logger.success(f"总数 {len(ytb_stream.keys())}")


def get_ytb(url,headers):
    try:
        query = urlparse(url).query
        query_dict = parse_qs(query)
        stream_id = query_dict['v'][0]
    except:
        msg = f"url格式解析失败 {url}"
        logger.error(msg)
        return msg
    if ytb_stream.get(stream_id) is not None:
        if ytb_stream[stream_id]["expire"] > time.time()-60:            
            logger.success(f"从缓存加载直播源 {url}")
        else:
            logger.info(f"youtube直播源已过期 {url}")
            update_ytb(url,headers,stream_id)
    else:
        logger.info(f"youtube直播源不存在 {url}")
        update_ytb(url,headers,stream_id)
    stream_url = "/proxy?url="+ytb_stream[stream_id]['stream_url']
    data = "#EXTM3U\n#EXTINF:\n"+stream_url
    return data
        
    



def splicing(url, query_params):
    url_parsed = list(urlparse(url))
    temp_para = parse_qsl(url_parsed[4])
    temp_para.extend(parse_qsl(query_params.__str__()))
    url_parsed[4] = urlencode(temp_para)
    url_new = urlunparse(url_parsed)
    return url_new

