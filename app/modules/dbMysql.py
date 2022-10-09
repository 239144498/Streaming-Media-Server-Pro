#!/usr/bin python3
# -*- coding: utf-8 -*-
# @Author: Naihe
# @Email: 239144498@qq.com
# @Software: Streaming-Media-Server-Pro
import time
import pymysql
import contextlib
from pymysql.cursors import DictCursor, Cursor

from app.settings import mysql_cfg


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

    # 通过以下两个方法判断mysql是否连通，以及重连。
    def is_connected(self, num=3600, stime=3):
        # num = 28800
        _number = 0
        _status = True
        while _status and _number <= num:
            """Check if the server is alive"""
            try:
                self.connection.ping(reconnect=True)  # ping 校验连接是否异常
                _status = False
            except:
                if self.re_connect():  # 重新连接,成功退出
                    _status = False
                    break
                _number += 1
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


if __name__ == '__main__':
    mysql = get_mysql_conn()
    sql = 'SELECT * FROM video ORDER BY ctime DESC LIMIT 1'
    result = mysql.fetchone(sql)
    print(result)
    mysql.close()
