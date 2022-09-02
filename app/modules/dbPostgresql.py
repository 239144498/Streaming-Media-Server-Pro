#!/usr/bin python3
# -*- coding: utf-8 -*-
from psycopg2 import pool
from psycopg2.extras import DictCursor, execute_batch

from app.settings import cfg, postgre_cfg


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
            cursor = DictCursor
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

    def fetchone(self, sql):
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

    def fetchall(self, sql, size=-1):
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


def get_postgre_conn():
    config = {
        'host': postgre_cfg['host'],
        'port': int(postgre_cfg['port']),
        'dbName': postgre_cfg['database'],
        'dbUser': postgre_cfg['user'],
        'dbPassword': postgre_cfg['password'],
        'sslMode': '',
        'sslRootCert': ''
    }
    return PostgreSql(config)


if __name__ == '__main__':
    cur = get_postgre_conn()
    sql = 'SELECT * FROM video ORDER BY ctime DESC LIMIT 1'
    # sql = "SELECT content FROM video where vname='{}'".format("123.ts")
    result = cur.fetchone(sql)
    print(result['vcontent'].tobytes())
