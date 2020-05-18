from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler
import logg
import settings
import threading
import time
from ethadress import get_eth_address
import database
from ensdata.app import get_domains

import traceback
def error(update, context, error):
    """Log Errors caused by Updates."""
    logg.ERROR.warning('Update "%s" caused error "%s", error: %s', update, context, error)
    logg.ERROR.warning(traceback.format_exc())

def handle_inline_result(bot, update):
    query = update.callback_query
    print(query)
    query.answer()
    query.edit_message_text(text="Selected option: {}".format(query.data))

def handle_update_message(bot, update):
    if update.message.text == "/start":
        eth_adress = get_eth_address(update.effective_user.id)
        if not eth_adress:
            update.message.reply_text("Could not find linked ethereum address")
            return
        domains = get_domains(eth_adress)
        update.message.reply_html(
            database.Domains.insert_domains(domains, eth_adress, update.effective_user.id)
        )
    elif update.message.text == "/list":
        update.message.reply_html(
            database.Domains.list(update.effective_user.id)
        )
    else:
        update.message.reply_text("Please try /start or /list")

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(settings.BOT_TOKEN)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, handle_update_message))
    dp.add_handler(MessageHandler(Filters.command, handle_update_message))
    dp.add_handler(CallbackQueryHandler(handle_inline_result))
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    t = threading.current_thread()
    while True:
        if not getattr(t, "do_run", True):
            updater.stop()
            break
        time.sleep(1)