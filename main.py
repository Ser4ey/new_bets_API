import time

from chromdriver_class import FireFoxDriverMain
from API_worker import APIWorker1
from data import AccountsBet365


# просто ставки на bet365 без проверок
account1 = AccountsBet365[0]
driver1 = FireFoxDriverMain('0.5')
driver1.log_in_bet365(account1['bet365_login'], account1['bet365_password'])

while True:
    bet_type = input('bet type:')
    coef = 0
    url = input('bet url:')

    driver1.make_cyber_football_bet(
                url=url,
                bet_type=bet_type,
                coef=coef
            )




