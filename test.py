from chromdriver_class import FireFoxDriverMain, FireFoxForPimatch
from data import AccountsBet365, path_to_accounts_file
import datetime
from multiprocessing.dummy import Pool
import time
from API_worker import APIWorker1
import random
from telegram_API import telegram_notify1


def make_bet_multipotok(All_elements_array):
    print('Ставим ставку на одном из аккаунтов')
    driver, sport, url, bet_type, coef = All_elements_array
    try:
        driver.make_any_sport_bet(sport, url, bet_type, coef)
    except Exception as er:
        print(f'Ошибка при проставлении ставки: {er}')
        driver.reanimaite_bet365com()


def reanimate_bet365com(driver):
    driver.reanimaite_bet365com()


def register_bet365_multipotok(AccountData):
    driver2, login, password = AccountData[0], AccountData[1], AccountData[2]
    time.sleep(random.randint(10, 500)/100)
    print(f'Open bet365 for: {login}')

    while True:
        try:
            r = driver2.open_bet365com()
        except:
            print(f'! Перезагрузка драйвера для {login}')
            driver2.restart_driver()
            continue
        if r is None:
            break
        else:
            print('-'*100)
            print(f'Сайт bet365 не загрузился для {login}')
            print('-'*100)
            driver2.restart_driver()
            time.sleep(5)

    try:
        driver2.log_in_bet365(login, password)
    except:
        print('!'*100)
        print(f'Не удалось войти в аккаунт {login}')
        print('!'*100)


def cheeck_porezan_li_account(driver):
    driver.check_is_account_not_valid_mean_porezan()


def delete_account_from_txt_by_login(login: str):
    '''Удаляет из файла с аккаунтами все строки, содержащии данный логин'''
    with open(path_to_accounts_file, 'r', encoding='utf-8') as file:
        lines_with_accounts = file.readlines()

    with open(path_to_accounts_file, 'w', encoding='utf-8') as file:
        for line in lines_with_accounts:
            if not login in line:
                file.write(line)
            else:
                print(f'{login} - удалён из аккаунтов!')
    return


# driverParimatch = FireFoxForPimatch()

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

AllBetsSet = set()

while True:
    driver = List_of_bet_account[0]
    sport = 'basketball'
    coef = '0'

    # input('reanimate:')
    # with Pool(processes=len(List_of_bet_account)) as p:
    #     A = [i for i in List_of_bet_account]
    #     p.map(reanimate_bet365com, A)
    bet_type = 'SET_01__WIN__P2'
    bet_type = input('bet type:')
    url = input('url:')

    driver.make_any_sport_bet(sport, url, bet_type, coef)



