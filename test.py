from chromdriver_class import FireFoxDriverMain, FireFoxForPimatch
from data import AccountsBet365
import datetime
from multiprocessing.dummy import Pool
import time


driver1 = FireFoxForPimatch()

while True:
    bet_type = input('bet type:')
    url = input('url:')
    a = driver1.find_coef(url, bet_type)
    print(a)







