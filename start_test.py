from chromdriver_class import FireFoxDriverMain, FireFoxForPimatch
from data import AccountsBet365
import datetime
from multiprocessing.dummy import Pool
import time
import random


def register_bet365_multipotok(AccountData):
    driver2, login, password = AccountData[0], AccountData[1], AccountData[2]
    print(f'Вход в аккаунт: {login}')

    while True:
        r = driver2.open_bet365com()
        if r is None:
            break
        else:
            print('Сайт bet365 не загрузился')

    while True:
        try:
            driver2.log_in_bet365(login, password)
            break
        except:
            try:
                driver2.driver.close()
                driver2.driver.quit()
                print(f'Аккаунт {login} перезапускается')
            except:
                pass


list_of_start_info = []
List_of_bet_account = []

i1 = 1
for i in range(len(AccountsBet365)):
    print(f'Запуск аккаунта {i1}')
    account_data = AccountsBet365[i]

    driver2 = FireFoxDriverMain(account_data['bet_value'])
    List_of_bet_account.append(driver2)
    start_info = [driver2, account_data['bet365_login'], account_data['bet365_password']]

    list_of_start_info.append(start_info)

    i1 += 1


with Pool(processes=len(list_of_start_info)) as p:
    p.map(register_bet365_multipotok, list_of_start_info)

