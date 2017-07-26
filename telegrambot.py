import atexit
import sys

import re
import telegram
from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler

from UpdateThread import UpdateThread
from currencies import currencies
from db import store_log, connection

if len(sys.argv) > 1:
    token = sys.argv[1]
else:
    print('Token not provided!')
    sys.exit()

regex = {
    'BYN': r'^(\d+((\.|\,)\d+)?)(\s*BYN)?$',
    'USD': r'^(\d+((\.|\,)\d+)?)\s*(\$|USD)$',
    'EUR': r'^(\d+((\.|\,)\d+)?)\s*(\€|EUR)$',
    'RUR': r'^(\d+((\.|\,)\d+)?)\s*(\₽|RUR)$',
}


def find_currency(text: str):
    for key, r in regex.items():
        result = re.match(r, text)
        if result is not None:
            return {
                'currency': key,
                'amount': float(result.groups()[0].replace(',', '.'))
            }
    return None


def message(bot: Bot, update: Update) -> None:
    try:
        input_data = find_currency(update.message.text)
        if input_data is None:
            response = 'Неверный формат!'
        elif input_data['currency'] == 'BYN':
            response = '\U0001F1E7\U0001F1FE BYN ' + '{0:g}'.format(input_data['amount']) + 'руб.'
            for currency in currencies:
                amount = input_data['amount'] / currency.amount
                response += '\n' + currency.icon + ' ' + currency.name + ' ' + '{0:g}'.format(amount) + currency.suf
        else:
            response = 'Выбранная валюта пока не поддерживается!'
    except:
        response = 'Произошла непредвиденная ошибка!'
    update.message.reply_text(response)
    store_log(update, response)


def command_help(bot: Bot, update: Update) -> None:
    update.message.reply_text('*Отправьте сообщение в одном из форматов:*\n'
                              '1000 - будет считаться как BYN\n'
                              '1000 BYN\n'
                              '1000 USD\n'
                              '1000 $\n'
                              '1000 EUR\n'
                              '1000 €\n'
                              '1000 RUR\n'
                              '1000 ₽\n', parse_mode=telegram.ParseMode.MARKDOWN)


update_thread = UpdateThread()
update_thread.start()

updater = Updater(token)

updater.dispatcher.add_handler(MessageHandler(Filters.text, message))
updater.dispatcher.add_handler(CommandHandler('help', command_help))

updater.start_polling()
updater.idle()

atexit.register(lambda: connection.close())
