from chromdriver_class import FireFoxFonbet
import datetime
from multiprocessing.dummy import Pool
import time


driverFavbet = FireFoxFonbet()

while True:
    bet_type = input('bet_type:')
    url = input('url:')
    second_coef = driverFavbet.find_coef_for_any_sport('volleyball', url, bet_type)
    print(second_coef)

