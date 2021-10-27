from chromdriver_class import FireFoxDriverMain, FireFoxForPimatch
import datetime
from multiprocessing.dummy import Pool
import time


driverParimatch = FireFoxForPimatch()

while True:
    url = input('url:')
    second_coef = driverParimatch.find_coef_for_any_sport('basketball', url, 'WIN_OT__P2')
    print(second_coef)

