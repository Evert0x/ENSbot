import database
import time
import threading
import settings
from telegram import Bot
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

def do():
    bot = Bot(settings.BOT_TOKEN)
    print(bot.id)
    for expires in database.Domains.get_expires():
        print(expires.userid)
        bot.send_message(
            chat_id=expires.userid,
            text="Your domains %s.ens is about to expire, do you want to extend?" % expires.domain,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                text="1 year",
                # function-gwei-args
                callback_data="renew-10500000-name:%s-duration:%d" % (expires.domain, 60*60*24*365)
            )]])
        )

    time.sleep(60)


def run():
    t = threading.current_thread()
    while True:
        if not getattr(t, "do_run", True):
            return
        do()
        time.sleep(1)
