import time

from chromdriver_class import FireFoxDriverMain, FireFoxForPimatch
from API_worker import APIWorker1
from data import AccountsBet365


driver1 = FireFoxForPimatch()

# for i in range(100):
#     time.sleep(10)
#
#     fork_info = APIWorker1.send_request_to_API()
#     if not fork_info:
#         print('no forks')
#         continue
#     print(fork_info['parimatch_type'])
#     # info = driver1.get_all_coef_from_url(fork_info['parimatch_href'])
#     coef = driver1.find_coef(fork_info['parimatch_href'], fork_info['parimatch_type'])
#     print(coef)
#

for i in range(100):
    bet_type = input('bet_type:')
    url_ = input('url:')

    coef = driver1.find_coef(url_, bet_type)
    print(coef)






