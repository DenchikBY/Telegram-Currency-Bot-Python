from random import randint
from typing import List


class Currency:
    amount: float = 0
    name: str = None
    icon: str = None
    suf: str = None
    bank_code: int = None

    def __init__(self, name: str, icon: str, suf: str, bank_code: int) -> None:
        super().__init__()
        self.amount = randint(1, 100)
        self.name = name
        self.icon = icon
        self.suf = suf
        self.bank_code = bank_code


currencies: List[Currency] = [
    Currency('USD', '\U0001F1FA\U0001F1F8', '$', 145),
    Currency('EUR', '\U0001F1EA\U0001F1FA', '€', 292),
    Currency('RUR', '\U0001F1F7\U0001F1FA', 'руб.', 298),
]
