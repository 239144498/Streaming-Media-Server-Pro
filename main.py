import uvicorn
from threading import Thread
from app.routers import app
from app.settings import PORT, localhost
from app.utile import everyday

if __name__ == '__main__':
    Thread(target=everyday, args=(2,)).start()
    print(localhost)
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")  # reload=True, debug=True
