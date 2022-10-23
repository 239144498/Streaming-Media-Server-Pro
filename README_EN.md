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
- [REST API Guide](#rest-api-guide)
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

REST API Guide
---
[https://stream.naihe.cf/docs](https://stream.naihe.cf/docs)  
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

Channels are now supported
---
- [x] MinTV Radio 1
- [x] MinTV Taiwan
- [x] MinTV
- [x] Big Love TV
- [x] CTV
- [x] CTV Classic
- [x] China TV
- [x] Sanli General TV
- [x] Hakka TV
- [x] Eight Variety Channel
- [x] CTV Elite
- [x] TVBS
- [x] Alta Entertainment
- [x] Jingtian General Channel
- [x] Jingtian Japan
- [x] New Tang Dynasty Asia Pacific
- [x] CTS
- [x] ARIRANG Arirang Channel
- [x] LiveABC Interactive English Channel
- [x] Da Vinci Channel
- [x] ELTV Living English Channel
- [x] Nick Jr. Kids Channel
- [x] Nick Kids Channel
- [x] Jing Tian Cartoon Channel
- [x] Jing Yang Cartoon Nice Bingo
- [x] i-Fun Anime Channel
- [x] MOMO Parent-Child Channel
- [x] CN Cartoon
- [x] Easton Shopping One
- [x] Mirror TV News Channel
- [x] ETTV News
- [x] China TV News
- [x] MinTV News
- [x] Sanli Financial News iNEWS
- [x] TVBS News
- [x] ETTV News
- [x] CTS News
- [x] Zhongtian News
- [x] SBN Global News
- [x] SBN Global Finance
- [x] TVBS
- [x] Easton Shopping 2
- [x] MinTV Variety
- [x] Porky's Cabaret Show
- [x] Jing Tian Yu Le Channel
- [x] KLT-Jing Tian International
- [x] Nice TV 靖天快乐台
- [x] Jing Tian Info Channel
- [x] ZhongTian's Biggest Party
- [x] TVBS Joy
- [x] Korea Entertainment Channel KMTV
- [x] Lifetime Entertainment Channel
- [x] Movie Soundtrack CMusic
- [x] TRACE Urban
- [x] MTV Live HD Music Channel
- [x] Mezzo Live HD
- [x] CLASSICA Classical
- [x] BOSS Highball
- [x] BOSS Sports One
- [x] BOSS Infinity
- [x] BOSS Tennis Table
- [x] TRACE Sport Stars
- [x] TRACE Sport Stars
- [x] Fashion Sports X
- [x] Car Fans TV
- [x] GINX Esports TV
- [x] TechStorm
- [x] Pet Club TV
- [x] MinTV Travel Channel
- [x] Rolling Power Rollor
- [x] Asia Travel Channel
- [x] Happy Space Home
- [x] Love Nature
- [x] History History Channel
- [x] Smithsonian Channel
- [x] Elda Life Travel Channel
- [x] LUXE TV Channel
- [x] TV5MONDE STYLE HD Life & Style
- [x] Zhongtian Gourmet Travel
- [x] PBS Drama
- [x] MinTV Drama Channel
- [x] LW Drama Channel
- [x] HITS Channel
- [x] Lung Wah Japanese and Korean Channel
- [x] Eight Wonderful Stages
- [x] Jing Tian Drama Channel
- [x] Jing Yang Drama Channel
- [x] CI Crime Investigation Channel
- [x] Sena Haren Documentary Channel
- [x] Fans Digital Documentary Channel
- [x] Kinko's Bunko
- [x] ROCK Extreme
- [x] Zaichang Movie & Drama
- [x] Jingtian Film
- [x] Jing Tian Cinema
- [x] Long Hua Film Channel
- [x] Fans Digital Movie Channel
- [x] amc favourite movies
- [x] CinemaWorld
- [x] CATCHPLAY Beyond
- [x] CATCHPLAY Movie Channel
- [x] My Cinema Europe HD
- [x] Good News 2
- [x] Good News
- [x] Big Love 2
- [x] People TV
- [x] Al Jazeera International News
- [x] VOA Voice of America
- [x] CNBC Asia
- [x] DW Deutsche Welle
- [x] CNN Headline News
- [x] CNN International News
- [x] Capitol Channel 1
- [x] Capitol Channel 2
- [x] Classic Movies
- [x] Classic Cartoons
- [x] Selected Anime Channel
- [x] Chinese Drama
- [x] Chinese Variety Channel
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

![](https://ik.imagekit.io/naihe/pay/zsm.png)

**&emsp;&emsp;The `star` or `sponsorship` you give on GitHub is what keeps me going for a long time, thank you from the bottom of my heart to each and every supporter, "every time you spend money you're voting for the world you want". Also, recommending this project to as many people as possible is a way to support it, the more people who use it the more motivation there is to update it.**
