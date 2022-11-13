#!/usr/bin python3
# -*- coding: utf-8 -*-

import os
import time
from loguru import logger
from app.conf import config


class Vfile():
    def __init__(self):
        self.datadir = config.datadir
        if not os.path.isdir(self.datadir):
            os.makedirs(self.datadir)
            logger.warning('已创建视频缓存路径：' + self.datadir)

    def file_get(self, subpath):
        self.filepath = os.path.join(self.datadir, subpath)
        try:
            with open(self.filepath, 'rb') as f:
                content = f.read()
        except Exception as e:
            logger.error('读取文件失败：' + self.filepath + str(e))
            return None

        if len(content) > 1024:
            logger.debug('读取文件成功：' + self.filepath)
        else:
            logger.warning('读取文件异常：' + self.filepath + ' 文件大小' + str(len(content)))
        return content

    def file_store(self, subpath, content):
        self.filepath = os.path.join(self.datadir, subpath)
        if len(content) == 0:
            logger.error('写入文件为空')
        else:
            try:
                with open(self.filepath, 'wb') as f:
                    f.write(content)
                logger.debug('写入文件成功：' + self.filepath)
                return True
            except Exception as e:
                logger.error('写入文件失败：' + self.filepath + str(e))
                return False

    def clean_file(self, timeout=180):
        # 删除存在时间超过180秒的文件
        cnt = 0
        for f in os.listdir(self.datadir):
            path = os.path.join(self.datadir, f)
            st_mtime = os.stat(path).st_mtime
            if time.time() > st_mtime + timeout:
                cnt += 1
                os.remove(path)
        return cnt


# 创建文件接口对象
vfile = Vfile()
