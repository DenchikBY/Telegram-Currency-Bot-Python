import threading

import time

import requests
import sys

from currencies import currencies


class UpdateThread(threading.Thread):
    def run(self) -> None:
        super().run()
        while True:
            try:
                for currency in currencies:
                    r = requests.get('http://www.nbrb.by/API/ExRates/Rates/' + str(currency.bank_code)).json()
                    currency.amount = r['Cur_OfficialRate'] / r['Cur_Scale']
                    print(currency.name + ': ' + str(currency.amount) + currency.suf)
            except:
                print('Не получайтся спарсить курсы валют!')
                sys.exit()
            time.sleep(3600)
