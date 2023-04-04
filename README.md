<div align="center">
  
[Streaming-Media-Server-Pro](https://github.com/239144498/Streaming-Media-Server-Pro)
-------------
[![builds](https://github.com/239144498/Streaming-Media-Server-Pro/actions/workflows/docker-image.yml/badge.svg)](https://github.com/239144498/Streaming-Media-Server-Pro/actions/workflows/docker-image.yml)
[![Netlify Status](https://api.netlify.com/api/v1/badges/31776721-e836-4042-a22a-3afe29ff1824/deploy-status)](https://app.netlify.com/sites/nowtv/deploys)  
[![Python version](https://img.shields.io/badge/python->=3.8-green.svg?style=plastic&logo=python)](https://www.python.org/downloads/release/python-380/)
[![Docker pulls](https://img.shields.io/docker/pulls/239144498/streaming.svg?style=plastic&logo=docker)](https://hub.docker.com/r/239144498/streaming)
[![GitHub stars](https://img.shields.io/github/stars/239144498/Streaming-Media-Server-Pro?color=brightgreen&style=plastic&logo=Apache%20Spark)](https://github.com/239144498/Streaming-Media-Server-Pro/stargazers)
[![MIT license](https://img.shields.io/badge/license-GNU3.0-green.svg?style=plastic&logo=React%20Hook%20Form)](https://github.com/239144498/Streaming-Media-Server-Pro/blob/main/LICENSE)

Documentation: [English version](https://github.com/239144498/Streaming-Media-Server-Pro/blob/main/README_EN.md) | 中文版

</div>

[更新日志](https://github.com/239144498/Streaming-Media-Server-Pro/wiki/%E6%9B%B4%E6%96%B0%E6%97%A5%E5%BF%97)
---

- 我创建了`IPTV频道`群组，可供交流、测试、反馈， **加入可直接访问 [https://t.me/+QmBC4d4jtgo2M2M9](https://t.me/+QmBC4d4jtgo2M2M9) ，或者扫码加入：**

<a href="https://t.me/+QmBC4d4jtgo2M2M9"><img src="https://ik.imagekit.io/naihe/github/img.png" alt="stream.png" border="0" width="220px" height="220px" /></a>



目录
-------------------
- [项目树形图](#项目树形图)
- [公益视频网站](#公益视频网站)
- [核心功能](#核心功能)
- [程序接口指南](#程序接口指南)
- [播放效果](#播放效果)
- [原理介绍](#原理介绍)
- [文字详解](#文字详解)
- [使用方式](#使用方式)
  - [python部署:](#python部署)
  - [安装依赖](#安装依赖)
  - [运行](#运行)
- [License](#License)

项目树形图
---

```
.
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── log
│   ├── api
│   │   ├── __init__.py
│   │   ├── a4gtv
│   │   │   ├── __init__.py
│   │   │   ├── endecrypt.py
│   │   │   ├── generateEpg.py
│   │   │   ├── tasks.py
│   │   │   ├── tools.py
│   │   │   └── utile.py
│   │   └── v2
│   │       ├── __init__.py
│   │       └── endpoints
│   │           ├── __init__.py
│   │           ├── more.py
│   │           └── sgtv.py
│   ├── assets
│   │   ├── EPG.xml
│   │   ├── diyepg.txt
│   ├── common
│   │   ├── __init__.py
│   │   ├── costum_logging.py
│   │   ├── diyEpg.py
│   │   ├── gitrepo.py
│   │   └── header.py
│   ├── conf
│   │   ├── __init__.py
│   │   ├── config.ini
│   │   └── config.py
│   ├── db
│   │   ├── __init__.py
│   │   ├── DBtools.py
│   │   └── dbMysql.py
│   └── scheams
│       ├── __init__.py
│       └── basic.py
├── main.py
├── requirements.txt
├── Dockerfile
├── README.md
├── Procfile
└── LICENSE

```

核心功能
---

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
- 支持反向代理或使用CDN（负载均衡）

程序接口指南
---
[https://stream.naihe.cf/docs](https://stream.naihe.cf/docs)  
<img src="https://ik.imagekit.io/naihe/github/apilist.png" title="api列表"/>

播放效果
---

<img src="https://ik.imagekit.io/naihe/github/1.png" title="播放效果" alt=""/>

<img height="600" src="https://ik.imagekit.io/naihe/github/4.png" title="节目单&频道表" alt=""/>

原理介绍
---
如下图所示：
<img src="https://ik.imagekit.io/naihe/github/%E5%8E%9F%E7%90%86%E7%A4%BA%E6%84%8F%E5%9B%BE.jpg" title="原理图"/>

文字详解
---
图中多台服务器是一种理想情况下实现，实际python程序、redis和mysql都可以在同一台服务器中实现
- ① 客户端请求m3u8文件
   - 1-> 查看内存是否缓存，否则服务器执行图流程2
   - 2-> BackgroundTasks任务：执行图流程3，分布式下载数量根据设置的缓冲区大小决定
    - 3<- 返回m3u8文件
- ② 客户端请求ts片
   - 1-> 查看本地是否缓存，否则服务器执行图流程2
   - 2-> BackgroundTasks任务：执行图流程3
   - 3-> 查看内存是否已下载完成状态，下载完执行图流程4，否则循环判断等待
   - 4<- 返回ts文件
- ③ 还有很多技术细节就不一一展开，只列出以上部分  

该项目根据分析4gtv网站的接口，通过算法得到生成ts视频的一些关键参数，省去请求网站从而得到m3u8文件的通信时长等开销，针对海外视频网站被墙隔离，支持以下几种观看方式：
- 通过**具有缓冲区的中转服务**观看（调用api接口 /online.m3u8）
- 通过**CDN**或**反向代理**观看（调用api接口 /channel.m3u8?&host=xxx）
- 使用**科学上网软件**观看（调用api接口 /channel2.m3u8）  

使用方式
---
> 💡提示：最好将本项目部署至美国地区的服务器，否则可能会出现奇怪的BUG。

推荐大家使用[Digitalocean](https://www.digitalocean.com/?refcode=45e25f5e4569&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)的服务器，主要是因为免费。

<a href="https://www.digitalocean.com/?refcode=45e25f5e4569&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge"><img src="https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%201.svg" alt="DigitalOcean Referral Badge" /></a>

使用我的邀请链接注册，你可以获得$200的credit，当你在上面消费$25时，我也可以获得$25的奖励。

我的邀请链接：

[https://m.do.co/c/45e25f5e4569](https://m.do.co/c/45e25f5e4569)
> 根据以下通用命令部署本项目
### python部署: 
python版本>=3.8+
``` code
git clone https://github.com/239144498/Streaming-Media-Server-Pro.git
```
### 安装依赖
``` code
pip install -r requirements.txt
```
### 运行
``` code
python3 main.py
```

**（docker部署）更多使用教程详情 https://www.cnblogs.com/1314h/p/16651157.html**

现已支持频道
---
- [x] 在diychannel.txt文件添加自定义频道

License
---
[GNU-3.0 © naihe](https://github.com/239144498/Streaming-Media-Server-Pro/blob/main/LICENSE)

