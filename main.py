import time

from chromdriver_class import FireFoxDriverMain
from API_worker import APIWorker1
from data import AccountsBet365


# просто ставки на bet365 без проверок
account1 = AccountsBet365[0]
driver1 = FireFoxDriverMain(account1['bet_value'])
driver1.log_in_bet365(account1['bet365_login'], account1['bet365_password'])


AllBetsSet = set()

while True:
    for i in range(100):
        time.sleep(15)

        fork_info = APIWorker1.send_request_to_API()

        if not fork_info:

            continue
        print(fork_info)

        if fork_info['fork_id'] in AllBetsSet:
            print(f"Ставка {fork_info['fork_id']} уже проставлена!")
            time.sleep(10)
            continue
        AllBetsSet.add(fork_info['fork_id'])

        driver1.make_cyber_football_bet(
            url=fork_info['bet365_href'],
            bet_type=fork_info['bet365_type'],
            coef=fork_info['bet365_coef']
        )


    AllBetsSet = set()







