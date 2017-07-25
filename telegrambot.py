import atexit
import sys

from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters

from UpdateThread import UpdateThread
from currencies import currencies
from db import store_log, connection

if len(sys.argv) > 1:
    token = sys.argv[1]
else:
    print('Token not provided!')
    sys.exit()


def message(bot: Bot, update: Update) -> None:
    try:
        input_val = float(update.message.text.replace(',', '.'))
        response = '\U0001F1E7\U0001F1FE BYN ' + '{0:g}'.format(input_val) + 'руб.'
        for currency in currencies:
            amount = input_val / currency.amount
            response += '\n' + currency.icon + ' ' + currency.name + ' ' + '{0:g}'.format(amount) + currency.suf
    except:
        response = 'Неверный формат!'
    update.message.reply_text(response)
    store_log(update, response)


update_thread = UpdateThread()
update_thread.start()

updater = Updater(token)

updater.dispatcher.add_handler(MessageHandler(Filters.text, message))

updater.start_polling()
updater.idle()

atexit.register(lambda: connection.close())
