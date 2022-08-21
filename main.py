import os
import uvicorn
from threading import Thread

from app.main import app
from app.settings import PORT
from app.utile import everyday


if __name__ == '__main__':
    Thread(target=everyday, args=(2,)).start()
    print(os.environ['local'])
    # uvicorn.run(app='app.main:app', host="127.0.0.1", port=15000, reload=True, debug=True)
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")
