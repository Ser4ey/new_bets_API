import time

from chromdriver_class import FireFoxDriverMain, FireFoxForPimatch
from API_worker import APIWorker1
from data import AccountsBet365


driver1 = FireFoxForPimatch()

for i in range(100):
    time.sleep(10)

    fork_info = APIWorker1.send_request_to_API()
    if not fork_info:
        print('no forks')
        continue
    print(fork_info)
    info = driver1.get_all_coef_from_url(fork_info['parimatch_href'])
    
    print(info)











