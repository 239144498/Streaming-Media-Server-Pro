#!/usr/bin python3
# -*- coding: utf-8 -*-
# @Author: Naihe
# @Email: 239144498@qq.com
# @Software: Streaming-Media-Server-Pro
import uvicorn
from app.api import app
from app.conf.config import PORT


if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port=PORT, log_level="info")

