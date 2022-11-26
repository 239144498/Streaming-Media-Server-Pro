# -*- coding: utf-8 -*-
# @Time    : 2022/10/12
# @Author  : Naihe
# @Email   : 239144498@qq.com
# @File    : tasks.py
# @Software: PyCharm
import requests
from loguru import logger

from app.conf import config
from app.conf.config import repoState
from app.plugins.a4gtv.utile import get
from app.db.localfile import vfile  # 新增本地文件处理模块


def gotask():
    get.filename.clear()
    if repoState:
        with requests.get("https://agit.ai/239144498/demo/raw/branch/master/4gtvchannel.xml") as res:
            with open(config.ROOT / "assets/EPG.xml", "wb") as f:
                f.write(res.content)
    logger.success("今日任务完成")


def sqltask():
    # 保留最新100条缓存，避免长时间运行内存溢出
    keys = list(get.filename)
    keys.reverse()
    _ = {}
    if len(keys) > 100:
        for index, element in enumerate(keys):
            if index < 100:
                _.update({element: get.filename.get(element)})
        get.filename = _
    logger.success("get.filename 删除完成")


def filetask():
    # 保留最近3分钟的视频文件，避免占用过多磁盘空间
    cnt = vfile.clean_file()
    logger.success('成功删除视频文件'+str(cnt)+'个')


if __name__ == '__main__':
    gotask()
