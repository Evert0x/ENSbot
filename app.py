from tg import main
from watcher import run
import time
import threading
import sys

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
    return True

app = create_app()

if __name__ == '__main__':
    while app:
        time.sleep(1)