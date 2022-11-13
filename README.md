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

> *&emsp;&emsp;在互联网快速发展的今天，有成千上万个用户都有观看电视的需求，而我，*
*想打造一个让每个人都拥有自己的电视频道的目标，每个人都可以根据自己的喜欢去筛选喜欢的节目，*
*并且拥有免费且流畅的观看体验。*

---
### &emsp;&emsp;_NEW_ 最新版来了，增加了对online接口本地缓存支持，项目增加模块化拓展，欢迎大家PR。

### &emsp;&emsp;新增对任意视频网站的视频流代理功能，解决了播放不同视频网站的跨域等问题。

### &emsp;&emsp;新增对程序结构性进行重构，网络请求改为异步+生成器方式，性能得到大幅提高；并且新增了日志管理和channel3接口，程序所有功能已基本完善，各位可否点亮star⭐。

---

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
- [现已支持频道](#现已支持频道)
- [📋 打赏名单 Donation List](#-打赏名单-donation-list)
- [❤ 打赏 Donation](#-打赏-donation)

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

公益视频网站
---

后端对接的本项目接口，可以在线观看接口内的所有电视。

https://player.naihe.cf  

![](https://ik.imagekit.io/naihe/enshan/img2.png)  

![](https://ik.imagekit.io/naihe/enshan/img1.png)  

核心功能
---

- 高效流媒体（具有缓冲区）
- 代理任意视频网站的视频流【_NEW_】
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
- [x] 民视第一台
- [x] 民视台湾台
- [x] 民视
- [x] 大爱电视
- [x] 中视
- [x] 中视经典台
- [x] 华视
- [x] 三立综合台
- [x] 客家电视台
- [x] 八大综艺台
- [x] 中视菁采台
- [x] TVBS精采台
- [x] 爱尔达娱乐台
- [x] 靖天综合台
- [x] 靖天日本台
- [x] 新唐人亚太台
- [x] 中天综合台
- [x] ARIRANG阿里郎频道
- [x] LiveABC互动英语频道
- [x] 达文西频道
- [x] ELTV生活英语台
- [x] Nick Jr. 儿童频道
- [x] 尼克儿童频道
- [x] 靖天卡通台
- [x] 靖洋卡通Nice Bingo
- [x] i-Fun动漫台
- [x] MOMO亲子台
- [x] CN卡通
- [x] 东森购物一台
- [x] 镜电视新闻台
- [x] 东森新闻台
- [x] 华视新闻
- [x] 民视新闻台
- [x] 三立财经新闻iNEWS
- [x] TVBS新闻
- [x] 东森财经新闻台
- [x] 中视新闻
- [x] 中天新闻台
- [x] 寰宇新闻台
- [x] SBN全球财经台
- [x] TVBS
- [x] 东森购物二台
- [x] 民视综艺台
- [x] 猪哥亮歌厅秀
- [x] 靖天育乐台
- [x] KLT-靖天国际台
- [x] Nice TV 靖天欢乐台
- [x] 靖天资讯台
- [x] 中天全民最大党
- [x] TVBS欢乐台
- [x] 韩国娱乐台 KMTV
- [x] Lifetime 娱乐频道
- [x] 电影原声台CMusic
- [x] TRACE Urban
- [x] MTV Live HD 音乐频道
- [x] Mezzo Live HD
- [x] CLASSICA 古典乐
- [x] 博斯高球台
- [x] 博斯运动一台
- [x] 博斯无限台
- [x] 博斯网球台
- [x] TRACE Sport Stars
- [x] 智林体育台
- [x] 时尚运动X
- [x] 车迷TV
- [x] GINX Esports TV
- [x] TechStorm
- [x] Pet Club TV
- [x] 民视旅游台
- [x] 滚动力rollor
- [x] 亚洲旅游台
- [x] 幸福空间居家台
- [x] Love Nature
- [x] History 历史频道
- [x] Smithsonian Channel
- [x] 爱尔达生活旅游台
- [x] LUXE TV Channel
- [x] TV5MONDE STYLE HD 生活时尚
- [x] 中天美食旅游
- [x] 公视戏剧
- [x] 民视影剧台
- [x] 龙华戏剧台
- [x] HITS频道
- [x] 龙华日韩台
- [x] 八大精彩台
- [x] 靖天戏剧台
- [x] 靖洋戏剧台
- [x] CI 罪案侦查频道
- [x] 视纳华仁纪实频道
- [x] 影迷数位纪实台
- [x] 金光布袋戏
- [x] ROCK Extreme
- [x] 采昌影剧台
- [x] 靖天映画
- [x] 靖天电影台
- [x] 龙华电影台
- [x] 影迷数位电影台
- [x] amc最爱电影
- [x] CinemaWorld
- [x] CATCHPLAY Beyond
- [x] CATCHPLAY电影台
- [x] My Cinema Europe HD 我的欧洲电影
- [x] 好消息2台
- [x] 好消息
- [x] 大爱二台
- [x] 人间卫视
- [x] 半岛国际新闻台
- [x] VOA美国之音
- [x] CNBC Asia 财经台
- [x] DW德国之声
- [x] CNN头条新闻台
- [x] CNN国际新闻台
- [x] 国会频道1
- [x] 国会频道2
- [x] 经典电影台
- [x] 经典卡通台
- [x] 精选动漫台
- [x] 华语戏剧台
- [x] 华语综艺台
- [x] 在diychannel.txt文件添加更多频道

📋 打赏名单 Donation List
---
非常感谢「 [这些用户](https://github.com/239144498/Streaming-Media-Server-Pro/wiki/Donation-List) 」对本项目的赞助支持！

❤ 打赏 Donation
---
  如果你觉得本项目对你有帮助，请考虑打赏本项目，以激励我投入更多的时间进行维护与开发。 If you find this project helpful, please consider supporting the project going forward. Your support is greatly appreciated.

> Every time you spend money, you're casting a vote for the kind of world you want. -- Anna Lappe

![](https://ik.imagekit.io/naihe/pay/zsm.png)

**&emsp;&emsp;你在GitHub给的`star`或者`赞助`是我长期维护此项目的动力所在，由衷感谢每一位支持者，“每一次你花的钱都是在为你想要的世界投票”。 另外，将本项目推荐给更多的人，也是一种支持的方式，用的人越多更新的动力越足。**

License
---
[GNU-3.0 © naihe](https://github.com/239144498/Streaming-Media-Server-Pro/blob/main/LICENSE)


## 免责声明
- 本程序为免费开源项目，供大家管理及观看IPTV频道，方便下载以及学习Python，使用时请遵守相关法律法规，请勿滥用；
- 本程序通过调用官方接口实现，无破坏官方接口行为；
- 本程序仅做重定向/流量转发，不拦截、存储、篡改任何用户数据；
- 在使用本程序之前，你应了解并承担相应的风险，希望使用此程序仅以学习为目的，任何商业用途或侵害他人权利等行为造成的后果自行承担，与本程序无关；
- 如有侵权，请通过[邮件](239144498@qq.com)与我联系，会及时处理。
