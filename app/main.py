#!/usr/bin python3
# -*- coding: utf-8 -*-
import uvicorn
from threading import Thread
from app.settings import PORT, localhost
from app.routers import app
from app.utile import everyday


if __name__ == '__main__':
    Thread(target=everyday, args=(2,)).start()
    print(localhost)
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")   # reload=True, debug=True

# https://github.com/239144498/Streaming-Media-Server-Pro/workflows/docker-image/badge.svg?branch=main
# https://github.com/<OWNER>/<REPOSITORY>/workflows/<WORKFLOW_NAME>/badge.svg?branch=<branch-name>