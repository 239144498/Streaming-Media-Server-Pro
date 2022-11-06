#!/usr/bin python3
# -*- coding: utf-8 -*-
# @Time    : 2022/10/7
# @Author  : Naihe
# @Email   : 239144498@qq.com
# @File    : dbMysql.py
# @Software: PyCharm
import pymysql
import redis
from loguru import logger

from app.conf.config import redis_cfg, defaultdb
from app.db.dbMysql import get_mysql_conn

logger.info("正在检测数据库连接状态...")


def connect_redis():
    try:
        cur = redis.StrictRedis(
            host=redis_cfg['host'],
            port=int(redis_cfg['port']),
            password=redis_cfg['password'],
            ssl=False,
            decode_responses=True,
            health_check_interval=30,
        )
        cur.setex("1", 1, 1)
        redisState = True
        logger.success("redis已连接")
    except:
        cur = None
        redisState = False
        logger.warning("redis连接失败")
    return cur, redisState


cur, redisState = connect_redis()

if defaultdb == "mysql":
    try:
        DBconnect = get_mysql_conn()
        print(DBconnect.ping())
        logger.success("mysql已连接")
    except pymysql.err.OperationalError:
        DBconnect = None
        logger.warning("mysql连接失败")
else:
    DBconnect = None
    logger.warning("mysql连接失败")
