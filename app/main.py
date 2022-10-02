#!/usr/bin python3
# -*- coding: utf-8 -*-
# @Author: Naihe
# @Email: 239144498@qq.com
# @Software: Streaming-Media-Server-Pro
import uvicorn
from threading import Thread
from app.settings import PORT
from app.routers import app
from app.utile import everyday


if __name__ == '__main__':
    Thread(target=everyday, args=(2,)).start()
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")   # reload=True, debug=True