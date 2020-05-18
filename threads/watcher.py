import database
import time
import threading
import settings
from telegram import Bot
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import uuid
from ensdata.app import get_price
from settings import Web3

def do():
    bot = Bot(settings.BOT_TOKEN)
    for expires in database.Domains.get_expires():

        w1 = str(uuid.uuid4()).replace("-", "")[:10]
        y1 = str(uuid.uuid4()).replace("-", "")[:10]

        week1_duration = 60 * 60 * 24 * 7
        year1_duration = 60 * 60 * 24 * 365

        gwei_price = 0.00000021 # eth 210
        week1 = get_price(expires.domain, week1_duration)
        year1 = get_price(expires.domain, year1_duration)

        week_price = round(float(gwei_price * week1), 2)
        year_price = round(float(gwei_price * year1), 2)

        msg = bot.send_message(
            chat_id=expires.userid, 
            text="Your domain <b>%s.eth</b> is about to expire on %s, do you want to extend?" % (
                expires.domain, expires.expires.ctime()),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                text="1 year ($%s)" % year_price,
                # function-gwei-args
                callback_data="%s-renew-%s-%s-%d" % (y1, year1, expires.domain, year1_duration)
            ), InlineKeyboardButton(
                text="1 week ($%s)" % week_price,
                # function-gwei-args
                callback_data="%s-renew-%s-%s-%d" % (w1, week1, expires.domain, week1_duration)
            )]]),
            parse_mode="html"
        )

        database.Extend.add(
            expires.userid,
            expires.domain,
            msg.message_id,
            [(y1, "1 year"), (w1, "1 week")]
        )

    time.sleep(60)


def run():
    t = threading.current_thread()
    while True:
        if not getattr(t, "do_run", True):
            return
        do()
        time.sleep(1)
