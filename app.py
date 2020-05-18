from tg import main
from watcher import run
import time
import threading,settings
import sys
from server import app as flaskapp
from msgqueue import run as msgrun
threads = []

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    for thread in threads:
        thread.do_run = False
        thread.join()
    sys.exit(0)

def interrupt():
    signal_handler(None, None)

def create_app():
    global threads
    t1 = threading.Thread(name="tgbot", target=main)
    t1.start()
    threads.append(t1)

    t2 = threading.Thread(name="expire", target=run)
    t2.start()
    threads.append(t2)

    t3 = threading.Thread(name="msgqueue", target=msgrun)
    t3.start()
    threads.append(t3)
    return flaskapp

app = create_app()

if __name__ == '__main__':
    app.run(settings.FLASK_HOST, settings.FLASK_PORT)