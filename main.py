import time

from chromdriver_class import FireFoxDriverMain
from API_worker import APIWorker1
from data import AccountsBet365

account1 = AccountsBet365[0]
driver1 = FireFoxDriverMain(account1['bet_value'])
driver1.log_in_bet365(account1['login'], account1['password'])


for i in range(100):
    time.sleep(10)

    fork_info = APIWorker1.send_request_to_API()
    if not fork_info:
        print('no forks')
        continue









