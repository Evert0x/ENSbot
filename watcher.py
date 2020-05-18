import database
import time
import threading
import settings
from telegram import Bot
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import uuid


def do():
    bot = Bot(settings.BOT_TOKEN)
    for expires in database.Domains.get_expires():
        y1 = str(uuid.uuid4()).replace("-", "")[:10]
        d1 = str(uuid.uuid4()).replace("-", "")[:10]
        msg = bot.send_message(
            chat_id=expires.userid,
            text="Your domains %s.eth is about to expire, do you want to extend?" % expires.domain,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                text="1 year",
                # function-gwei-args
                callback_data="%s-renew-10500000-%s-%d" % (y1, expires.domain, 60*60*24*365)
            ), InlineKeyboardButton(
                text="1 day",
                # function-gwei-args
                callback_data="%s-renew-30000-%s-%d" % (d1, expires.domain, 60*60*24)
            )]])
        )

        database.Extend.add(
            expires.userid,
            expires.domain,
            msg.message_id,
            [(y1, "1 year"), (d1, "1 day")]
        )

    time.sleep(60)


def run():
    t = threading.current_thread()
    while True:
        if not getattr(t, "do_run", True):
            return
        do()
        time.sleep(1)
