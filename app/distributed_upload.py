#!/usr/bin python3
# -*- coding: utf-8 -*-
import time
import datetime
import psycopg2
import pymysql
import requests
from fastapi import FastAPI, Response
from pymysql.cursors import SSCursor

app = FastAPI()

DB_CONFIG = {
    'host': '192.x.91.34',
    'user': 'root',
    'password': '123456789',
    'port': 3306,
    'database': 'media',
    'charset': 'utf8'
}
conf = {
    'host': '192.x.91.34',
    'port': '5432',
    'dbName': 'media',
    'dbUser': 'root',
    'dbPassword': '123456789',
    'sslMode': '',
    'sslRootCert': ''
}


@app.get('/')
def abc():
    return Response(status_code=403, content="no access")


# 上传图片到数据库
def uploadts(vname, content, size):
    con = pymysql.connect(
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        charset=DB_CONFIG['charset'],
        autocommit=True
    )
    con.autocommit(True)
    query = 'insert into video(vname, vcontent, vsize) values(%s, %s, %s)'
    values = (vname, content, size)
    with con.cursor(SSCursor) as cursor:
        x = cursor.execute(query, values)  # 执行sql语句
        cursor.close()
    con.close()
    return x


@app.get("/url3/")
async def url3(url: str, filepath: str):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept-Encoding": "gzip, deflate, br",
    }
    a = time.time()
    repo = str(datetime.date.today())
    with requests.get(url=url, headers=header) as res:
        status = res.status_code
        content = res.content
        b = time.time()
        a1 = uploadts(filepath, content, len(content))
        c = time.time()
        print(c - a)
        print(b - a)
        print(c - b)
        print(a1)
        print(len(content))
        return {
            "总时长": round(c - a, 2),
            "请求": round(b - a, 2),
            "请求状态": status,
            "上传": round(c - b, 2),
            "上传状态": a1,
            "字长": len(content),
            "repo": repo
        }


def gp_connect():
    try:
        conn = psycopg2.connect(host=conf['host'], port=conf['port'], database=conf['dbName'],
                                                       user=conf['dbUser'], password=conf['dbPassword'],
                                                       connect_timeout=10)
        return conn
    except psycopg2.DatabaseError as e:
        print("could not connect to Greenplum server", e)


def uploadurl4(vname, content, size):
    query = "insert into video(vname, vcontent, vsize) values(%s, %s, %s)"
    values = (vname, psycopg2.Binary(content), size)
    try:
        with gp_connect() as conn:
            with conn.cursor() as cur:
                x = cur.execute(query, values)
                cur.close()
            conn.commit()
            return x
    except Exception as e:
        print(e)
        print('-------except')
        conn.close()
    finally:
        conn.close()


@app.get("/url4/")
async def download435(url: str, filepath: str):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    a = time.time()
    repo = str(datetime.date.today())
    with requests.get(url=url, headers=header) as res:
        status = res.status_code
        content = res.content
        b = time.time()
        a1 = uploadurl4(filepath, content, len(content))
        c = time.time()
        print(c - a)
        print(b - a)
        print(c - b)
        print(a1)
        print(len(content))
        return {
            "总时长": round(c - a, 2),
            "请求": round(b - a, 2),
            "请求状态": status,
            "上传": round(c - b, 2),
            "上传状态": a1,
            "字长": len(content),
            "repo": repo
        }


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
