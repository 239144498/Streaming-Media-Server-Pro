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
from app.db.dbMysql import get_mysql_conn, init_database

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

def mysql_connect_test():
    try:
        DBconnect = get_mysql_conn()
        print(DBconnect.ping())
        logger.success("mysql已连接")
        return DBconnect, True
    except pymysql.err.OperationalError as e:
        DBconnect = None
        logger.error(e)
        logger.error("mysql连接失败")
        return DBconnect, False


if defaultdb == "mysql":
    # 尝试初始化，创建video表，然后再连接
    try:
        init_database()
        logger.success("mysql已创建初始化表")
    except pymysql.err.OperationalError as e:
        logger.error(e)
        logger.error("mysql初始化表失败")
    DBconnect, sqlState = mysql_connect_test()
else:
    DBconnect = None
    sqlState = False
    logger.warning("defaultdb未配置mysql")