#!/usr/bin python3
# -*- coding: utf-8 -*-
import redis
from app.modules.dbMysql import get_mysql_conn
from app.modules.dbPostgresql import get_postgre_conn
from app.settings import redis_cfg, defaultdb
from loguru import logger

try:
    logger.info("检测redis连接")
    cur = redis.StrictRedis(
        host=redis_cfg['host'],
        port=int(redis_cfg['port']),
        password=redis_cfg['password'],
        ssl=True,
        decode_responses=True,
        health_check_interval=30,
    )
    cur.setex("1", 1, 1)
    redisState = True
    logger.info("redis已连接")
except:
    cur = None
    redisState = False
    logger.warning("redis连接失败")


class DB(object):
    """
    对数据库进行封装，消除差异性
    """
    def __init__(self, x=1):
        if defaultdb == "mysql":
            if x:
                logger.info("检测mysql连接")
            self.dbname = "mysql"
            self.mysql = get_mysql_conn()
            if x:
                logger.info("mysql已连接")
        elif defaultdb == "postgresql":
            if x:
                logger.info("检测postgresql连接")
            self.dbname = "postgresql"
            self.postgre = get_postgre_conn()
            if x:
                logger.info("postgresql已连接")
        else:
            self.dbname = ""
            if x:
                logger.warning("数据库连接失败")

    def fetchone(self, sql):
        if self.dbname == "mysql":
            content = self.mysql.fetchone(sql)
            return content
        elif self.dbname == "postgresql":
            content = self.postgre.fetchone(sql)
            content.update({"vcontent": content['vcontent'].tobytes()})
            return content

    def fetchall(self, sql):
        if self.dbname == "mysql":
            content = self.mysql.fetchall(sql)
            return content
        elif self.dbname == "postgresql":
            content = self.postgre.fetchall(sql)
            return content

    def execute(self, sql, value):
        if self.dbname == "mysql":
            content = self.mysql.execute(sql, value)
            return content
        elif self.dbname == "postgresql":
            content = self.postgre.execute(sql)
            return content


DBconnect = DB()
