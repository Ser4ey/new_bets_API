from chromdriver_class import FireFoxForPimatch, FireFoxForWinline
import datetime
from multiprocessing.dummy import Pool
import time


driverParimatch = FireFoxForWinline()

while True:
    bet_type = input('bet_type:')
    url = input('url:')
    second_coef = driverParimatch.find_coef_for_any_sport('soccer', url, bet_type)
    print(second_coef)

