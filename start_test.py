from chromdriver_class import FireFoxDriverMain, FireFoxForPimatch
from data import AccountsBet365
import datetime
from multiprocessing.dummy import Pool
import time
import random


def register_bet365_multipotok(AccountData):
    bet_value, login, password = AccountData[0], AccountData[1], AccountData[2]
    t = random.randint(1, 1000)
    time.sleep(t/100)
    print(AccountData)


List_of_accounts_start_info = []

for i in range(len(AccountsBet365)):
    account_data = AccountsBet365[i]

    start_info = [account_data['bet_value'], account_data['bet365_login'], account_data['bet365_password']]
    List_of_bet_account.append(start_info)


with Pool(processes=len(List_of_bet_account)) as p:
    p.map(register_bet365_multipotok, List_of_bet_account)


# while True:
#     try:
#         driver2 = FireFoxDriverMain(account_data['bet_value'])
#         driver2.log_in_bet365(login=account_data['bet365_login'], password=account_data['bet365_password'])
#         List_of_bet_account[i] = driver2
#         break
#     except:
#         print('Ошибка при запуске аккаунта')
#         print(f'Повторный запуск аккаунта {i1}')
#         try:
#             driver2.driver.close()
#             driver2.driver.quit()
#         except:
#             pass
#
# i1 += 1
