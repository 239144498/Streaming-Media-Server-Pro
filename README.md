Streaming-Media-Server-Pro
-------------
&emsp;&emsp;在互联网快速发展的今天，有成千上万个用户都有观看电视的需求，而我，
想打造一个让每个人都拥有自己的电视频道的目标，每个人都可以根据自己的喜欢去筛选喜欢的节目，
并且拥有免费且流畅的观看体验。

核心功能
---
- 生成m3u
- 生成m3u8文件
- 视频中转（具有缓冲区）
- 异步下载视频
- 流媒体转发
- 生成[EPG节目单](https://agit.ai/239144498/demo/raw/branch/master/4gtvchannel.xml) 每日实时更新
- 分布式处理ts片段
- Redis缓存
- MySql或PostgreSql缓存
- 多服务器分流
- 清晰度可自定义
- 请求主机可自定义

REST API
---
[https://www.apifox.cn/apidoc/shared-95689a43-31f7-4ef2-952a-cecff34105f2/api-35577145](https://www.apifox.cn/apidoc/shared-95689a43-31f7-4ef2-952a-cecff34105f2/api-35577145)

实现效果：
---
#### ios软件观看效果

<img height="300" src="https://ik.imagekit.io/naihe/github/1.png?ik-sdk-version=javascript-1.4.3&updatedAt=1660959995410" title="播放效果" width="600"/>

<img height="600" src="https://ik.imagekit.io/naihe/github/2.png?ik-sdk-version=javascript-1.4.3&updatedAt=1660959995410" title="频道表" width="300"/>

<img height="600" src="https://ik.imagekit.io/naihe/github/3.png?ik-sdk-version=javascript-1.4.3&updatedAt=1660959995410" title="节目单" width="300"/>

原理介绍
---
如下图所示：
<img src="https://ik.imagekit.io/naihe/github/%E5%8E%9F%E7%90%86%E7%A4%BA%E6%84%8F%E5%9B%BE.jpg" title="原理图"/>

### **文字详解**
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
- 通过**具有缓冲区的中转服务**观看（调用api接口 online.m3u8）
- 通过**CDN**或**反向代理**观看（调用api接口 channel.m3u8?&host=xxx）
- 使用**科学上网软件**观看（调用api接口 channel2.m3u8）  

使用方式
---
#### Mysql操作
##### 创建数据库
``` 
CREATE DATABASE media
``` 
##### 创建video表
``` 
create table media.video(
    vname varchar(30) not null,
    CONSTRAINT video_pk PRIMARY KEY (vname),
    vcontent  MEDIUMBLOB NOT NULL,
    vsize varchar(20) NULL,
    ctime  timestamp(0) default now()
);
``` 
##### CIL执行，设置定时事件
``` 
SET GLOBAL event_scheduler = ON;

use video;

DROP event IF EXISTS auto_delete;
CREATE EVENT auto_delete
ON SCHEDULE EVERY 30 minute     # xx分钟根据数据库的存储和查询性能综合决定
DO
TRUNCATE video;
``` 
#### python部署:  
##### 命令终端执行
``` code
git clone https://github.com/239144498/Streaming-Media-Server-Pro.git
```
##### 安装依赖
``` code
pip install -r requirements.txt
```
##### 运行
``` code
python3 main.py
```
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
- [x] Global Trekker
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
- [x] HISTORY 2 频道
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

License
---
Released under the MIT license.

Copyright, 2022, by naihe,239144498@qq.com .

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

