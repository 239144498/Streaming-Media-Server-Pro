import time

import requests
from psycopg2 import pool
import pymysql
import contextlib
from pymysql.cursors import DictCursor as DictCursor1, Cursor, SSCursor
from psycopg2.extras import DictCursor as DictCursor2, execute_batch


class MySQLConnect(object):
    def __init__(self, cursorclass=DictCursor1, config=None):
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

    def execute(self, sql):
        self.is_connected()
        if sql:
            with self.cursor() as cursor:
                return cursor.execute(sql)

    def executemany(self, sql=None, data=None):
        self.is_connected()
        if sql and data:
            with self.cursor() as cursor:
                return cursor.executemany(sql, data)

    def task(self):
        self.is_connected()
        sql = 'select * from video order by ctime desc limit 10;'
        with self.cursor() as cursor:
            data = cursor.execute(sql)
            print(data)
            return data


def get_a_conn(cursorclass=DictCursor1):
    MYSQL_config = {
        'host': 'xxx',
        'user': 'root',
        'password': 'xxxx',
        'port': 55624,
        'database': 'video',
        'charset': 'utf8'
    }
    return MySQLConnect(cursorclass, MYSQL_config)


class PostgreSql(object):
    def __init__(self, config):
        try:
            # ThreadedConnectionPool
            # SimpleConnectionPool
            # PersistentConnectionPool
            self.connectPool = pool.ThreadedConnectionPool(2, 10, host=config['host'], port=config['port'],
                                                           database=config['dbName'],
                                                           user=config['dbUser'],
                                                           password=config['dbPassword'], keepalives=1,
                                                           keepalives_idle=30, keepalives_interval=10,
                                                           keepalives_count=5)
        except Exception as e:
            print(e)

    def getConnect(self, cursor=None):
        if not cursor:
            cursor = DictCursor2
        conn = self.connectPool.getconn()
        cursor = conn.cursor(cursor_factory=cursor)
        try:
            return conn, cursor
        except Exception as err:
            raise err

    def closeConnect(self, conn, cursor):
        cursor.close()
        self.connectPool.putconn(conn)

    def closeAll(self):
        self.connectPool.closeall()

    # 执行增删改
    def execute(self, sql, value=None):
        conn, cursor = self.getConnect()
        try:
            with conn:
                with cursor:
                    if value:
                        cursor.execute(sql, value)
                        res = cursor.rowcount
                    else:
                        cursor.execute(sql)
                        res = cursor.rowcount
                    conn.commit()
                    # if "delete" in sql:
                    #     sql = "VACUUM FULL video;"
                    #     cursor.execute(sql)
                    self.closeConnect(conn, cursor)
                    return res
        except Exception as e:
            self.closeConnect(conn, cursor)
            raise e

    def selectOne(self, sql):
        conn, cursor = self.getConnect()
        try:
            with conn:
                with cursor:
                    cursor.itersize = 1
                    cursor.execute(sql)
                    result = cursor.fetchone()
                    self.closeConnect(conn, cursor)
                    return result
        except Exception as e:
            self.closeConnect(conn, cursor)
            raise e

    def selectAll(self, sql, size=-1):
        conn, cursor = self.getConnect()
        try:
            with conn:
                with cursor:
                    cursor.itersize = 1
                    cursor.execute(sql)
                    result = cursor.fetchmany(size)
                    self.closeConnect(conn, cursor)
                    return result
        except Exception as e:
            self.closeConnect(conn, cursor)
            raise e


def get_a_conn2():
    config = {
        'host': 'xxxx',
        'port': '5433',
        'dbName': 'yugabyte',
        'dbUser': 'xxx',
        'dbPassword': 'xxxx',
        'sslMode': '',
        'sslRootCert': ''
    }
    return PostgreSql(config)
