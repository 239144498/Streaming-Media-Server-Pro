# -*- coding: utf-8 -*-
# @Time    : 2022/10/12
# @Author  : Naihe
# @Email   : 239144498@qq.com
# @File    : tasks.py
# @Software: PyCharm
import asyncio
from loguru import logger

from app.api.a4gtv.generateEpg import generateprog, postask
from app.common.gitrepo import agit
from app.conf import config
from app.conf.config import gdata, xmlowner, xmlaccess_token, xmlrepo, repoState
from app.api.a4gtv.utile import get


def gotask():
    get.filename.clear()
    if repoState:
        import platform
        get.inin_repo()
        if "Windows" in platform.platform():
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            asyncio.run(postask())
        else:
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            loop = asyncio.get_event_loop()
            task = asyncio.ensure_future(postask())
            loop.run_until_complete(asyncio.wait([task]))

        content = generateprog(gdata)
        filepath = "4gtvchannel.xml"
        agit(xmlaccess_token).update_repo_file(xmlowner, xmlrepo, filepath, content)
        with open(config.ROOT / "assets/EPG.xml", "wb") as f:
            f.write(content)
    logger.success("今日任务完成")


def sqltask():
    # 保留最近100条缓存，避免长时间运行内存溢出
    keys = list(get.filename)
    keys.reverse()
    _ = {}
    if len(keys) > 100:
        for index, element in enumerate(keys):
            if index < 100:
                _.update({element: get.filename.get(element)})
        get.filename = _
    logger.success("删除完成")


if __name__ == '__main__':
    gotask()
