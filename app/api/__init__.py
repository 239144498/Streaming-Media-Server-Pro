# -*- coding: utf-8 -*-
# @Time    : 2022/10/8
# @Author  : Naihe
# @Email   : 239144498@qq.com
# @File    : __init__.py
# @Software: PyCharm
import sys
import logging

from loguru import logger
from fastapi import FastAPI
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.conf import config
from app.common.costum_logging import InterceptHandler, format_record
from .a4gtv.tasks import gotask, sqltask, filetask  #新增文件删除模块
from .v2 import v2
from ..conf.config import DEBUG
from ..scheams.response import Response200


def init_app():
    app = FastAPI(
        title=config.TITLE,
        description=config.DESC,
        version=config.VERSION,
        contact=config.CONTACT,
        debug=DEBUG
    )
    logging.getLogger().handlers = [InterceptHandler()]
    logger.configure(handlers=[{"sink": sys.stdout, "level": logging.DEBUG, "format": format_record}])
    logger.add(config.LOG_DIR / "日志文件.log", encoding='utf-8', rotation="0:00", enqueue=True, serialize=False,
               retention="7 days",
               backtrace=True, diagnose=True)
    logger.debug('日志系统已加载')
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    return app


app = init_app()
app.include_router(v2)


@app.get('/', summary="首页")
async def index():
    return Response200(data="这是一个开源的IPTV服务项目，功能强大且适合任意平台。",
                       msg="了解更多请访问：https://github.com/239144498/Streaming-Media-Server-Pro", code=200)


@app.on_event("startup")
async def startup():
    import pytz
    executors = {
        'default': ThreadPoolExecutor(5),
        'processpool': ProcessPoolExecutor(2)
    }
    job_defaults = {
        'coalesce': True,  # 默认为新任务关闭合并模式（）
        'max_instances': 3  # 设置新任务的默认最大实例数为3
    }
    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.configure(executors=executors, job_defaults=job_defaults,
                        timezone=pytz.timezone('Asia/Shanghai'))
    # cron表达式
    # 0 0 * * 0-6 每天凌晨执行一次 更新epg
    # 0 * * * * 每1小时执行一次 清理缓存
    # */10 * * * * 每10分钟执行一次 清理缓存的视频文件
    scheduler.add_job(gotask, CronTrigger.from_crontab("0 0 * * 0-6"), max_instances=2, misfire_grace_time=120)
    scheduler.add_job(sqltask, CronTrigger.from_crontab("0 * * * *"), max_instances=3, misfire_grace_time=120)
    scheduler.add_job(filetask, CronTrigger.from_crontab("*/10 * * * *"), max_instances=3, misfire_grace_time=120)
    logger.info(scheduler.get_jobs())
    logger.info("已开启定时任务")
    scheduler.start()


@app.on_event("shutdown")
async def shutdown():
    global scheduler
    scheduler.shutdown()
    logger.info("已关闭定时任务")
