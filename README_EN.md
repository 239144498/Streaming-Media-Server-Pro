<div align="center">

[Streaming-Media-Server-Pro](https://github.com/239144498/Streaming-Media-Server-Pro)
-------------
[![builds](https://github.com/239144498/Streaming-Media-Server-Pro/actions/workflows/docker-image.yml/badge.svg)](https://github.com/239144498/Streaming-Media-Server-Pro/actions/workflows/docker-image.yml)
[![Netlify Status](https://api.netlify.com/api/v1/badges/31776721-e836-4042-a22a-3afe29ff1824/deploy-status)](https://app.netlify.com/sites/nowtv/deploys)  
[![Python version](https://img.shields.io/badge/python->=3.8-green.svg?style=plastic&logo=python)](https://www.python.org/downloads/release/python-380/)
[![Docker pulls](https://img.shields.io/docker/pulls/239144498/streaming.svg?style=plastic&logo=docker)](https://hub.docker.com/r/239144498/streaming)
[![GitHub stars](https://img.shields.io/github/stars/239144498/Streaming-Media-Server-Pro?color=brightgreen&style=plastic&logo=Apache%20Spark)](https://github.com/239144498/Streaming-Media-Server-Pro/stargazers)
[![MIT license](https://img.shields.io/badge/license-GNU3.0-green.svg?style=plastic&logo=React%20Hook%20Form)](https://github.com/239144498/Streaming-Media-Server-Pro/blob/main/LICENSE)

Documentation: English version | [中文版](https://github.com/239144498/Streaming-Media-Server-Pro)

</div>

>_&emsp;&emsp; In today's fast growing internet, there are thousands of users who have a need to watch TV, and I, 
want to create a goal that everyone has their own TV channel, where everyone can filter their favorite shows to their liking, 
and have a free and smooth viewing experience._ 

---
### &emsp;&emsp;The latest version of the program structural refactoring, network requests to asynchronous + generator way, performance has been greatly improved; and new log management, all the features of the program has been basically perfect, Please help to light up the star⭐.  

---

Contents
-------------------
- [Project tree diagram](#project-tree-diagram)
- [Public service video sites](#public-service-video-sites)
- [Core functions](#core-functions)
- [API reference](#api-reference)
- [Playback effects](#playback-effects)
- [Principle](#principle)
- [Text Detail](#text-detail)
- [Usage](#usage)
  - [python deployment:](#python-deployment)
  - [Installing dependencies](#installing-dependencies)
  - [Run](#run)
- [Channels are now supported](#channels-are-now-supported)
- [📋 Reward List Donation List](#-reward-list-donation-list)
- [❤ Donation](#-donation)

Project tree diagram
---

```
.
├── app
│ ├── __init__.py
│ ├── main.py
│ ├── api
│ │ ├── __init__.py
│ │ │ ├── a4gtv
│ │ │ │ ├── __init__.py
│ │ │ │ ├── endecrypt.py
│ │ │ │ ├─ generateEpg.py
│ │ │ │ ├── tasks.py
│ │ │ ├─ tools.py
│ │ │ │ └─ utile.py
│ │ │ └── v2
│ │ │ ├── __init__.py
│ │ │ └── endpoints
│ │ │ ├── __init__.py
│ │ ├── more.py
│ │ └── sgtv.py
│ ├── assets
│ │ ├── EPG.xml
│ │ ├── diyepg.txt
│ │ └── log
│ ├── common
│ │ ├── __init__.py
│ │ ├── costum_logging.py
│ │ ├── diyEpg.py
│ │ ├── gitrepo.py
│ │ ├── header.py
│ ├── conf
│ │ ├── __init__.py
│ │ ├── config.ini
│ │ └── config.py
│ ├── db
│ │ ├── __init__.py
│ │ ├── dbtools.py
│ │ └── dbMysql.py
│ └── scheams
│ ├── __init__.py
│ └── basic.py
├── main.py
├── requirements.txt
├── Dockerfile
├── README.md
├─ Procfile
└─ LICENSE

```

Public service video sites
---

The back-end interface to the project that allows you to watch all the TVs within the interface online.

[https://player.naihe.cf](https://player.naihe.cf)

![](https://ik.imagekit.io/naihe/enshan/img2.png)  

![](https://ik.imagekit.io/naihe/enshan/img1.png)  

Core functions
---

- Generate m3u files
- Generate m3u8 files
- Video staging (with buffer)
- Asynchronous download of videos
- Streaming and forwarding
- Generate [EPG programme listings](https://agit.ai/239144498/demo/raw/branch/master/4gtvchannel.xml) Live daily updates
- Distributed processing of ts clips
- Redis cache parameters
- MySql or PostgreSql caching of videos
- Forward proxy requests
- Custom addition of program channels
- Custom TV station labels
- Customizable clarity
- Reverse proxy or set of CDN requests (load balancing)

API reference
---
[https://stream.naihe.cf/redoc](https://stream.naihe.cf/redoc)  
<img src="https://ik.imagekit.io/naihe/github/apilist.png" title="api list"/>

Playback effects
---

<img src="https://ik.imagekit.io/naihe/github/1.png" title="Playback effects" alt=""/>

<img height="600" src="https://ik.imagekit.io/naihe/github/2.png" title="Channel list" alt=""/>

<img height="600" src="https://ik.imagekit.io/naihe/github/3.png" title="Programme List" alt=""/>

Principle
---
As shown in the image below.
<img src="https://ik.imagekit.io/naihe/github/%E5%8E%9F%E7%90%86%E7%A4%BA%E6%84%8F%E5%9B%BE.jpg" title="Schematic" />

Text Detail
---
The diagram of multiple servers is an ideal case implementation, the actual python program, redis and mysql can all be implemented in the same server
- ① Client requests m3u8 files
   - 1-> Check if memory is cached, otherwise server executes diagram flow 2
   - 2-> BackgroundTasks task: execute flow 3 of the diagram, the number of distributed downloads is determined by the set buffer size
    - 3<- Return m3u8 file
- ② Client request ts piece
   - 1-> Check if it is cached locally, otherwise the server executes flow 2
   - 2-> BackgroundTasks task: execute diagram flow 3
   - 3-> check if the memory has been downloaded to complete the state, the download is complete execution diagram flow 4, otherwise loop judgment wait
   - 4<- return ts file
- ③ There are many more technical details so I won't start one by one, just list the above parts  

The project is based on the analysis of the interface of the 4gtv website, through the algorithm to get some key parameters for generating ts video, eliminating the overhead of requesting the website and thus getting the communication length of m3u8 files, etc. For overseas video websites isolated by walls, the following viewing methods are supported.
- Watching via **relay service** with buffer (call api interface /online.m3u8)
- Watching via **CDN** or **reverse proxy** (call api interface /channel.m3u8?&host=xxx)
- Watching with **scientific internet software** (call api interface /channel2.m3u8)  

Usage
---
### python deployment: 
python version recommended 3.9+
``` code
git clone https://github.com/239144498/Streaming-Media-Server-Pro.git
```
### Installing dependencies
``` code
pip install -r requirements.txt
```
### Run
``` code
python3 main.py
```

**(docker deployment) More tutorial details https://www.cnblogs.com/1314h/p/16651157.html**


- [x] Add more channels to diychannel.txt file


📋 Reward List Donation List  
---
Many thanks to "[these users](https://github.com/239144498/Streaming-Media-Server-Pro/wiki/Donation-List)" for sponsoring this project!

❤ Donation
---
  If you find this project helpful, please consider donating to this project to motivate me to devote more time to maintenance and development. If you find this project helpful, please consider supporting the project going forward.

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/naihe)  

PayPal: [https://www.paypal.me/naihes](https://www.paypal.me/naihes)

> Every time you spend money, you're casting a vote for the kind of world you want. -- Anna Lappe

![](https://ik.imagekit.io/naihe/pay/hbm.jpg)

**&emsp;&emsp;The `star` or `sponsorship` you give on GitHub is what keeps me going for a long time, thank you from the bottom of my heart to each and every supporter, "every time you spend money you're voting for the world you want". Also, recommending this project to as many people as possible is a way to support it, the more people who use it the more motivation there is to update it.**

License
---
[GNU v3.0](https://github.com/239144498/Streaming-Media-Server-Pro/blob/main/LICENSE)

Disclaimers
---
- this program is a free open source project for you to manage and watch IPTV channels, to facilitate downloading and to learn Python, please observe the relevant laws and regulations when using it, please do not abuse it.
- this program is implemented by calling the official interface, no damage to the official interface.
- This program only does redirection/traffic forwarding, it does not intercept, store or tamper with any user data.
- **Before using this program, you should understand and bear the corresponding risk, hope to use this program only for learning purposes, any infringement of other people's interests, commercial use, damage to national reputation or other violations of the law and other acts caused by all the consequences of their own responsibility, not related to the author himself;**
- If there is any infringement, please contact me at [email](239144498@qq.com) and it will be dealt with promptly.

