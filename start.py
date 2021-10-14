import time

from chromdriver_class import FireFoxDriverMain, FireFoxForPimatch
from API_worker import APIWorker1
from data import AccountsBet365


driverParimatch = FireFoxForPimatch()

account1 = AccountsBet365[0]
driver1 = FireFoxDriverMain(account1['bet_value'])
driver1.log_in_bet365(account1['bet365_login'], account1['bet365_password'])


AllBetsSet = set()

while True:
    for i in range(100):
        time.sleep(5)

        fork_info = APIWorker1.send_request_to_API()

        if not fork_info:
            # print('no forks now')
            continue
        print(fork_info)

        if fork_info['fork_id'] in AllBetsSet:
            print(f"Ставка {fork_info['fork_id']} уже проставлена!")
            time.sleep(10)
            continue
        AllBetsSet.add(fork_info['fork_id'])

        second_coef = driverParimatch.find_coef(fork_info['parimatch_href'], fork_info['parimatch_type'])
        print(f'Коэффициент на париматч: {second_coef}')

        try:
            float(second_coef)
        except:
            print('Ставка не поддерживается')
            continue

        if float(second_coef) < float(fork_info['parimatch_coef']):
            print('Коэффициет на париматч упал!', f'{fork_info["parimatch_coef"]} -> {second_coef}')
            continue

        driver1.make_cyber_football_bet(
            url=fork_info['bet365_href'],
            bet_type=fork_info['bet365_type'],
            coef=fork_info['bet365_coef']
        )


    AllBetsSet = set()






