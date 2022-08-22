#!/usr/bin python3
# -*- coding: utf-8 -*-
import re
import json
import asyncio
import datetime
import time
import aiohttp
import requests
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from xml.dom.minidom import Document
from urllib import parse
from app.settings import *

requests.packages.urllib3.disable_warnings()
request = requests.session()


class agit:
    def __init__(self, access_token):
        self.headers = {
            "Connection": "keep-alive",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        self.access_token = access_token
        self.request = requests.session()

    def get_file_sha(self, owner, repo, filepath, branch="master", i=0):
        if i > 10:
            raise Exception("无法获取sha")
        url = f"https://xxxx/api/v1/repos/{owner}/{repo}/contents/{parse.quote_plus(filepath)}?ref={branch}&access_token={self.access_token}"
        with self.request.get(url=url, headers=self.headers, verify=False) as res:
            if res.status_code != 200:
                raise Exception(res.text)
            return res.json()['sha']

    def get_repo_sha(self, owner, repo, branch="master", i=0):
        url = f"https://xxxx/api/v1/repos/{owner}/{repo}/git/refs/heads/{branch}?access_token={self.access_token}"
        with self.request.get(url=url, headers=self.headers, verify=False) as res:
            if res.status_code != 200:
                raise Exception(res.text)
            return res.json()[-1]['object']['sha']

    def update_repo_file(self, owner, repo, filepath, content, branch="master", i=0):
        if i > 10:
            raise Exception("无法更新")
        url = f"https://xxxx/api/v1/repos/{owner}/{repo}/contents/{filepath}?access_token={self.access_token}"
        data = {
            "branch": branch,
            "content": b64encode(content).decode(),
            "sha": self.get_file_sha(owner, repo, filepath)
        }
        with self.request.put(url=url, json=data, headers=self.headers, verify=False) as res:
            return res.status_code

    def create_repo_file(self, owner, repo, filepath, content, branch="master", i=0):
        if i > 3:
            raise Exception("无法创建")
        url = f"https://xxx/api/v1/repos/{owner}/{repo}/contents/{filepath}?access_token={self.access_token}"
        data = {
            "branch": branch,
            "content": b64encode(content).decode(),
        }
        with self.request.post(url=url, json=data, headers=self.headers) as res:
            if res.status_code != 201:
                print(res.text)
                if res.status_code == 500:
                    return self.create_repo_file(owner, repo, filepath, content, i=i + 1)
            return res.status_code

    def delete_repo_file(self, owner, repo, filepath, branch="master", i=0):
        if i > 10:
            raise Exception("无法删除")
        url = f"https://xxx/api/v1/repos/{owner}/{repo}/contents/{filepath}?access_token={self.access_token}"
        data = {
            "branch": branch,
            "sha": self.get_file_sha(owner, repo, filepath)
        }
        with self.request.delete(url=url, json=data, headers=self.headers, verify=False) as res:
            return res.status_code

    def create_branch(self, owner, repo, branch_name):
        url = f"https://xxxx/api/v1/repos/{owner}/{repo}/branches?access_token={self.access_token}"
        data = {
            "new_branch_name": branch_name
        }
        with self.request.post(url=url, json=data, headers=self.headers, verify=False) as res:
            return res.status_code

    def delete_branch(self, owner, repo, branch_name):
        url = f"https://xxxx/api/v1/repos/{owner}/{repo}/branches/{branch_name}?access_token={self.access_token}"
        with self.request.delete(url=url, headers=self.headers, verify=False) as res:
            return res.status_code

    def cat_branch(self, owner, repo):
        """
        查看所有分支
        :param owner:
        :param repo:
        :return:
        """
        url = f"https://xxxx/api/v1/repos/{owner}/{repo}/branches?access_token={self.access_token}"
        with self.request.get(url=url, headers=self.headers, verify=False) as res:
            return [i['name'] for i in res.json()]

    def cat_repo(self, owner, repo):
        url = f"https://xxxx/api/v1/repos/{owner}/{repo}?access_token={self.access_token}"
        with self.request.get(url=url, headers=self.headers, verify=False) as res:
            return res.status_code

    def cat_repo_file_name(self, owner, repo, branchname="master"):
        """
        获取根目录的所有条目的元数据
        :param owner:
        :param repo:
        :return:
        """
        url = f"https://xxx/api/v1/repos/{owner}/{repo}/contents?ref={branchname}&access_token={self.access_token}"
        with self.request.get(url=url, headers=self.headers, verify=False) as res:
            return res.json()

    def cat_repo_tree(self, owner, repo, reposha):
        url = f"https://xxx/api/v1/repos/{owner}/{repo}/git/trees/{reposha}?access_token={self.access_token}"
        with self.request.get(url=url, headers=self.headers, verify=False) as res:
            return res.json()

    def get_single_file_state(self, owner, repo, filename, branchname="master"):
        url = f"https://xxx/api/v1/repos/{owner}/{repo}/contents/{filename}?ref={branchname}&access_token={self.access_token}"
        with self.request.get(url=url, headers=self.headers, verify=False) as res:
            return res.status_code

    def create_repo(self, name):
        url = f"https://xxxx/api/v1/user/repos?access_token={self.access_token}"
        data = {
            "auto_init": True,
            "name": name,
            "private": False,
        }
        with self.request.post(url=url, json=data, headers=self.headers, verify=False) as res:
            return res.status_code

    def delete_repo(self, owner, repo):
        url = f"https://xxx/api/v1/repos/{owner}/{repo}?access_token={self.access_token}"
        with self.request.delete(url=url, headers=self.headers, verify=False) as res:
            return res.status_code


def generatehead(tvdoc):
    tv = tvdoc.createElement("tv")
    tv.setAttribute("generator-info-name", "Generated by Naihe, 239144498@qq.com ")
    tv.setAttribute("generator-info-url", "https://xxxxxxx")
    tvdoc.appendChild(tv)
    return tv


def generatebody1(tvdoc, tv, var):
    # channel 标签
    channel = tvdoc.createElement("channel")
    channel.setAttribute("id", str(var['fnID']))

    # display-name
    display_name = tvdoc.createElement("display-name")
    display_name.setAttribute("lang", "zh")
    # display-name 标签中的值
    display_name_var = tvdoc.createTextNode(var['fsNAME'])
    display_name.appendChild(display_name_var)
    # 添加到channel节点
    channel.appendChild(display_name)
    # 添加到根标签
    tv.appendChild(channel)


def generatebody2(tvdoc, tv, channel, data):
    TIME_ZONE = " +0800"
    for var in eval(data):
        start = var['sdate'].replace("-", "") + var['stime'].replace(":", "")
        stop = var['edate'].replace("-", "") + var['etime'].replace(":", "")
        pname = var['title']

        programme = tvdoc.createElement("programme")
        title = tvdoc.createElement("title")
        text = tvdoc.createTextNode(pname)

        programme.setAttribute("start", start + TIME_ZONE)
        programme.setAttribute("stop", stop + TIME_ZONE)
        programme.setAttribute("channel", channel)

        title.setAttribute("lang", "zh")

        title.appendChild(text)
        programme.appendChild(title)

        tv.appendChild(programme)


def generateprog(tvlist):
    tvdoc = Document()
    tv = generatehead(tvdoc)
    for var1 in tvlist:
        generatebody1(tvdoc, tv, var1)

    cursor1, data1 = cur.hscan(str(datetime.date.today()), cursor=0, count=70)
    cursor2, data2 = cur.hscan(str(datetime.date.today()), cursor=cursor1, count=70)
    data1.update(data2)
    tvs = data1
    for k, v in tvs.items():
        generatebody2(tvdoc, tv, k, v)
    return tvdoc.toprettyxml(indent="\t", encoding="UTF-8")


async def download(fid, now, i=0):
    if i > 10:
        raise Exception(f"下载节目单{fid}失败")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    }
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f"https://xxxx/proglist/{fid}.txt") as res:
                res.encoding = "utf-8"
                return cur.hset(now, fid, await res.text())
    except:
        return await download(fid, now, i + 1)


######################################


async def postask():
    start = time.time()
    print(start)
    now = str(datetime.date.today())
    fids = str(cur.hkeys(now))
    tasks = []
    for fid in idata.keys():
        if fid in fids:
            continue
        tasks.append(download(fid, now))
    await asyncio.gather(*tasks)
    end = time.time()
    print("耗时: %s" % (end - start))
    cur.expire(now, 432000)


def decrypt(info):
    ciphertext = b64decode(info["Data"])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    info = json.loads(plaintext.decode('utf-8'))
    link = info["flstURLs"][1]
    return link


def now_time():
    return int(time.time())


def solve4gtv(x1, x2, now, gap):
    seq = round((now - x2) / gap)
    begin = round(seq * gap + x1)
    return seq, begin


def solveftv(now, x1):
    return round(now / idata[fid]["x"] - x1)


def solvelive(now, t1, t2, gap):
    x = now - t1
    seq = round(t2 + x // gap)
    return seq


def generate_m3u(host, hd, name):
    """
    构造 m3u 数据
    :param now:
    :param hd:
    :param name: online | channel | channel2
    :return:
    """
    yield '#EXTM3U x-tvg-url=""\n'
    for i in gdata():
        # tvg-ID="" 频道id匹配epg   fsLOGO_MOBILE
        yield '#EXTINF:{} tvg-chno="{}" tvg-id="{}" tvg-name="{}" tvg-logo="{}" group-title="{}",{}\n'.format(
            -1, i['fnCHANNEL_NO'], i['fs4GTV_ID'], i['fsNAME'],
            i['fsHEAD_FRAME'].replace("4gtvimg.4gtv.tv", "video.naihe1.workers.dev"), i['fsTYPE_NAME'], i['fsNAME'])
        if hd == "720":
            # yield host + f"/channel?fid={i['fs4GTV_ID']}\n"
            yield host + f"/{name}?fid={i['fs4GTV_ID']}\n"
        else:
            yield host + f"/{name}?fid={i['fs4GTV_ID']}&hd={hd}\n"


def writefile(filename, content):
    with open(filename, "wb") as f:
        f.write(content)
        f.close()


def get_4gtv(url):
    header = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        # "Connection": "close",
    }
    with request.get(url=url, headers=header, verify=False) as res:
        return res.text


def encrypt(fs4GTV_ID, fnID):
    raw = {"fnCHANNEL_ID": fnID, "fsASSET_ID": fs4GTV_ID, "fsDEVICE_TYPE": "pc",
           "clsIDENTITY_VALIDATE_ARUS": {
               "fsVALUE": "xxx+xxx+xxx/xxx+xxx+xxx/xxx+xx+xx/+x/xx=="}}
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = bytes(json.dumps(raw), 'utf-8')
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    value = b64encode(ciphertext).decode('utf-8')
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
    }
    url = "https://xxxxxxx" # 通过代理请求重要参数
    data = {
        "jsonrpc": "2.0",
        "method": "httpRequest",
        "id": 1,
        "params": {
            "url": "https://xxx/",
            "postData": {'value': value}
        }
    }
    with request.post(url=url, json=data, headers=headers, verify=False) as res:
        return res.json()


def genftlive(url):
    start = time.time()
    data = get_4gtv(url)
    seq = re.findall("#EXT-X-MEDIA-SEQUENCE:(\d+)\n", data).pop()
    gap = re.findall("#EXT-X-TARGETDURATION:(\d+)\n", data).pop()
    return start, int(seq), int(gap)


def get4gtvurl(fs4GTV_ID, fnID, hd):
    info = encrypt(fs4GTV_ID, fnID)
    link = decrypt(json.loads(info['result']))
    return re.sub(r"(\w+\.m3u8)", HD[hd], link)


def generate_url(fid, host, hd, begin, seq, url):
    if "4gtv-4gtv" in fid or "litv-ftv10" in fid or "litv-longturn17" == fid or "litv-longturn18" == fid:
        return url.format(host, begin, seq)
    elif "4gtv-live" in fid:
        return url.format(host, fid, f"{hd}{seq}")
    else:
        return url.format(host, seq)

