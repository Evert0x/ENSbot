from tg import main
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
    return True

app = create_app()

if __name__ == '__main__':
    while app:
        time.sleep(1)