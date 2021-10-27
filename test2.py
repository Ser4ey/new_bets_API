from chromdriver_class import FireFoxDriverMain, FireFoxForPimatch
import datetime
from multiprocessing.dummy import Pool
import time


driverParimatch = FireFoxForPimatch()

while True:
    bet_type = input('bet_type:')
    url = input('url:')
    second_coef = driverParimatch.find_coef_for_any_sport('basketball', url, bet_type)
    print(second_coef)

