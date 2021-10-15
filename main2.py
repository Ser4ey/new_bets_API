import time

from chromdriver_class import FireFoxDriverMain, FireFoxForPimatch
from API_worker import APIWorker1
from data import AccountsBet365

account1 = AccountsBet365[0]
driver1 = FireFoxDriverMain('%2')
driver1.log_in_bet365(account1['bet365_login'], account1['bet365_password'])

driver1.get_balance('%2')
driver1.get_balance('%3')
driver1.get_balance('%20')
driver1.get_balance('%200')


