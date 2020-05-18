import threading, time, database
from telegram import Bot
import settings
from datetime import datetime
from web3 import Web3

def do():
    bot = Bot(settings.BOT_TOKEN)
    s = database.Session()
    for d in database.Domains.get_all(s):
        q = settings.CONTRACT_ENS_WS.events.NameRenewed.createFilter(
            fromBlock=d.block,
            toBlock='latest',
            argument_filters={
                "name": d.domain
            }
        )

        for renewal in q.get_all_entries():
            newtimestamp = datetime.fromtimestamp(renewal["args"]["expires"])
            if newtimestamp > d.expires:
                d.expires = newtimestamp
                d.block = renewal["blockNumber"]


                extend = database.Extend.get(s, Web3.toHex(renewal["transactionHash"]))
                if extend:
                    extend.completed = True
                    bot.send_message(
                        text="Renewal for %s.ens completed!, <a href=\"%s/tx/%s\">link</a>" % (
                            d.domain,
                            settings.ETHERSCAN, str(Web3.toHex(renewal["transactionHash"]))),
                        chat_id=extend.userid,
                        reply_to_message_id=extend.msg_id,
                        parse_mode="html",
                        disable_web_page_preview=True
                    )
                else:
                    bot.send_message(
                        text="Unexpected renewal for %s.ens! <a href=\"%s/tx/%s\">link</a>" % (
                            d.domain,
                            settings.ETHERSCAN, str(Web3.toHex(renewal["transactionHash"]))),
                        chat_id=d.userid,
                        parse_mode="html",
                        disable_web_page_preview=True
                    )
                s.commit()
    s.close()

def run():
    t = threading.current_thread()
    while True:
        if not getattr(t, "do_run", True):
            return
        do()
        time.sleep(30)
        time.sleep(1)
