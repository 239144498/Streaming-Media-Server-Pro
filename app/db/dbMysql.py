#!/usr/bin python3
# -*- coding: utf-8 -*-
import time
import pymysql
import contextlib

from loguru import logger
from pymysql.cursors import DictCursor, Cursor

from app.conf.config import mysql_cfg


class MySQLConnect(object):
    def __init__(self, cursorclass=DictCursor, config=None):
        self.MYSQL_config = config
        self.cursorclass = cursorclass
        self.connection = pymysql.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            db=config['database'],
            cursorclass=cursorclass,
            charset=config['charset']
        )
        self.connection.autocommit(True)

    def ping(self):
        self.connection.ping(reconnect=True)  # ping 校验连接是否异常

    # 通过以下两个方法判断mysql是否连通，以及重连。
    def is_connected(self, num=3600, stime=3):
        # num = 28800
        _number = 0
        _status = True
        while _status and _number <= num:
            """Check if the server is alive"""
            try:
                self.ping()
                _status = False
            except:
                if self.re_connect():  # 重新连接,成功退出
                    _status = False
                    break
                _number += 1
                logger.info(f"mysql连接失败，正在第{_number}次重连...")
                time.sleep(stime)  # 连接不成功,休眠3秒钟,继续循环，知道成功或重试次数结束

    def re_connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.MYSQL_config['host'],
                port=self.MYSQL_config['port'],
                user=self.MYSQL_config['user'],
                password=self.MYSQL_config['password'],
                db=self.MYSQL_config['db'],
                cursorclass=self.cursorclass,
                charset=self.MYSQL_config['charset']
            )
            self.connection.autocommit(True)
            return True
        except:
            return False

    @contextlib.contextmanager
    def cursor(self, cursor=None):
        """通过yield返回一个curosr对象
        """
        cursor = self.connection.cursor(cursor)
        try:
            yield cursor
        except Exception as err:
            self.connection.rollback()
            raise err
        finally:
            cursor.close()

    def close(self):
        self.connection.close()

    def fetchone(self, sql=None):
        self.is_connected()
        if sql:
            with self.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchone()

        if self.connection.cursorclass == Cursor:
            return ()
        else:
            return {}

    def fetchall(self, sql=None):
        self.is_connected()
        if sql:
            with self.cursor() as cursor:
                cursor.execute(sql)
                return cursor.fetchall()
        return []

    def execute(self, sql, value):
        self.is_connected()
        if sql:
            with self.cursor() as cursor:
                return cursor.execute(sql, value)

    def executemany(self, sql=None, data=None):
        self.is_connected()
        if sql and data:
            with self.cursor() as cursor:
                return cursor.executemany(sql, data)


def get_mysql_conn(cursorclass=DictCursor):
    mysql_config = {
        'host': mysql_cfg['host'],
        'user': mysql_cfg['user'],
        'password': mysql_cfg['password'],
        'port': int(mysql_cfg['port']),
        'database': mysql_cfg['database'],
        'charset': 'utf8'
    }
    return MySQLConnect(cursorclass, mysql_config)

# 初始化数据库，创建database和表
def init_database(cursorclass=DictCursor):
    # 数据库账号需要拥有SUPER或SYSTEM_VARIABLES_ADMIN权限才能自动初始化
    mysql_config = {
        'host': mysql_cfg['host'],
        'user': mysql_cfg['user'],
        'password': mysql_cfg['password'],
        'port': int(mysql_cfg['port']),
        'database': 'mysql',
        'charset': 'utf8'
    }
    mysql = MySQLConnect(cursorclass, mysql_config)
    sql = "select count(1) cnt from information_schema.TABLES where TABLE_SCHEMA='media' and TABLE_NAME='video'"
    result = mysql.fetchone(sql)    
    
    if result['cnt']:
        logger.info("video表已存在")
    else:
        with mysql.connection.cursor() as cursor:
            cursor.execute('CREATE DATABASE media')
            cursor.execute('create table media.video(vname varchar(30) not null,CONSTRAINT video_pk PRIMARY KEY (vname),vcontent  MEDIUMBLOB NOT NULL,vsize varchar(20) NULL,ctime  timestamp(0) default now())')
            cursor.execute('SET GLOBAL event_scheduler = ON')
            cursor.execute('DROP event IF EXISTS media.auto_delete')
            cursor.execute('CREATE EVENT media.auto_delete ON SCHEDULE EVERY 30 minute DO TRUNCATE video')
        
    return '初始化数据库表完成'

if __name__ == '__main__':
    mysql = get_mysql_conn()
    sql = 'SELECT * FROM video ORDER BY ctime DESC LIMIT 1'
    result = mysql.fetchone(sql)
    print(result)
    mysql.close()
