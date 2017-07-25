import threading

import time
from datetime import datetime

import requests
import sys

from currencies import currencies


class UpdateThread(threading.Thread):
    def run(self) -> None:
        super().run()
        while True:
            message = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S") + ':'
            try:
                for currency in currencies:
                    r = requests.get('http://www.nbrb.by/API/ExRates/Rates/' + str(currency.bank_code)).json()
                    currency.amount = r['Cur_OfficialRate'] / r['Cur_Scale']
                    message += '\n' + currency.name + ': ' + str(currency.amount) + currency.suf
                print(message)
            except:
                print(message + '\nНе получайтся спарсить курсы валют!')
                sys.exit()
            time.sleep(3600)
