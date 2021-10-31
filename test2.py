from chromdriver_class import FireFoxFor1XBet, FireFoxForFavbet
import datetime
from multiprocessing.dummy import Pool
import time


driverFavbet = FireFoxForFavbet()

while True:
    bet_type = input('bet_type:')
    url = input('url:')
    second_coef = driverFavbet.find_coef_for_any_sport('soccer', url, bet_type)
    print(second_coef)

