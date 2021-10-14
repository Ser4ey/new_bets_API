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
            print('no forks now')
            continue
        print(fork_info)

        second_coef = driverParimatch.find_coef(fork_info['parimatch_href'], fork_info['parimatch_type'])
        if float(second_coef) < float(fork_info['parimatch_coef']):
            print('Коэффициет на париматч упал!')
            continue

        driver1.make_cyber_football_bet(
            url=fork_info['bet365_href'],
            bet_type=fork_info['bet365_type'],
            coef=fork_info['bet365_coef']
        )









