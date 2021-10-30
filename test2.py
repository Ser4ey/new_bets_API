from chromdriver_class import FireFoxForPimatch, FireFoxForWinline, FireFoxFor1XBet
import datetime
from multiprocessing.dummy import Pool
import time


driver1XBet = FireFoxFor1XBet()

while True:
    bet_type = input('bet_type:')
    url = input('url:')
    second_coef = driver1XBet.find_coef_for_any_sport('soccer', url, bet_type)
    print(second_coef)

