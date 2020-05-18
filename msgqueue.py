import threading
import time
import database
import datetime
import settings
from telegram import Bot

def do():
    bot = Bot(settings.BOT_TOKEN)
    s = database.Session()
    msgs = s.query(database.Queue).\
        filter(database.Queue.datetime <= datetime.datetime.utcnow()).all()

    for msg in msgs:
        bot.send_message(text=msg.text, chat_id=msg.chatid, reply_to_message_id=msg.replyid)
        s.delete(msg)
    s.commit()
    s.close()
    time.sleep(5)

def run():
    t = threading.current_thread()
    while True:
        if not getattr(t, "do_run", True):
            return
        do()
        time.sleep(1)