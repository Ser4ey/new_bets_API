from chromdriver_class import FireFoxDriverMainNoAutoOpen, GetWorkAccountsList
from data import AccountsBet365, path_to_accounts_file
import datetime
from multiprocessing.dummy import Pool
import time
from telegram_API import telegram_notify1
import data
from API_worker_valuebet import APIWorker1
import random

def make_bet_multipotok(All_elements_array):
    print('Ставим ставку на одном из аккаунтов')
    driver, sport, url, bet_type, coef = All_elements_array
    try:
        driver.make_any_sport_bet(sport, url, bet_type, coef)
    except Exception as er:
        print(f'Ошибка при проставлении ставки: {er}')
        driver.reanimaite_bet365com()

def reanimate_bet365com(driver):
    try:
        driver.reanimaite_bet365com()
    except:
        pass

def check_is_account_froze(driver):
    try:
        driver.restart_browser_and_bet365_account()
    except:
        pass


def cheeck_porezan_li_account(driver):
    try:
        driver.check_is_account_not_valid_mean_porezan()
    except Exception as er:
        print(f'Ошибка при определении порезки для - {driver.bet365_login}\nError: {er}')

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

def log_in_driver(driver_class):
    login = driver_class.bet365_login
    passwd = driver_class.bet365_password
    driver_class.log_in_bet365_v2(login, passwd)


def open_stable_bet365(driver_class):
    driver_class.restart_browser_and_bet365_account(check_valid=False)



List_of_Bet365_open = []
list_of_start_info = []

i1 = 1
for i in range(len(AccountsBet365)):
    account_data = AccountsBet365[i]
    start_info = [account_data['bet365_login'], account_data['bet365_password'], account_data['bet_value'], account_data['vpn_country']]
    list_of_start_info.append(start_info)
    i1 += 1


# запускаем аккаунты
List_of_bet_account = []
countries = []
Set_of_countries = set()

for i in list_of_start_info:
    countries.append(i[3])

for i in countries:
    Set_of_countries.add(i)

Dict_of_Drivers_count = {}

for i in Set_of_countries:
    Dict_of_Drivers_count[i] = countries.count(i)


start_time_for_all = time.time()
for i in Set_of_countries:
    print(f'Открываем {Dict_of_Drivers_count[i]} аккаунта для {i}')
    start_time_for_type = time.time()
    accounts_get_class = GetWorkAccountsList(number_of_accounts=Dict_of_Drivers_count[i], vpn_country=i)
    Accounts = accounts_get_class.return_Browser_List()

    for account_info in list_of_start_info:
        bet365login, bet365password, bet_value, vpn_country = account_info
        if vpn_country != i:
            continue

        driver_class = FireFoxDriverMainNoAutoOpen(
            driver=Accounts.pop(-1),
            login=bet365login,
            password=bet365password,
            bet_value=bet_value,
            vpn_country=vpn_country
        )

        List_of_bet_account.append(driver_class)
    print(f'{Dict_of_Drivers_count[i]} аккаунтов для {i} открыты за {time.time() - start_time_for_type}')

print(f'Все аккаунты успешно открыты за {time.time() - start_time_for_all}')
# авторизация аккаунтов
with Pool(processes=len(List_of_bet_account)) as p:
    p.map(log_in_driver, List_of_bet_account)

print(f'Все аккаунты успешно авторизованы!')
# START OF PROGRAM

porezan_counter = 1
# предварительный поиск порезанных аккаунтов
with Pool(processes=len(List_of_bet_account)) as p:
    p.map(cheeck_porezan_li_account, List_of_bet_account)
i_porez = 0
while i_porez < len(List_of_bet_account):
    if not List_of_bet_account[i_porez].is_valud_account:
        telegram_text = f'{List_of_bet_account[i_porez].bet365_login} - порезан. Баланс: {List_of_bet_account[i_porez].get_balance()} '
        telegram_notify1.telegram_bot_send_message(telegram_text)
        delete_account_from_txt_by_login(List_of_bet_account[i_porez].bet365_login)
        print(f'Аккаунт {List_of_bet_account[i_porez].bet365_login} - порезан')
        List_of_bet_account[i_porez].driver.quit()
        List_of_bet_account.pop(i_porez)
    else:
        i_porez += 1

print(f'Осталось рабочих аккаунтов: {len(List_of_bet_account)}')
# завершение поиска порезанных аккаунтов

AllBetsSet = set()

reboot_counter = 0
graphic_bet_telegram_counter = 0
error_flag = False

while True:
    for j1 in range(80):
        time.sleep(7)

        try:
            fork_info = APIWorker1.send_request_to_API(old_bets_set=AllBetsSet)
            if not fork_info:
                continue
            print(fork_info)
        except Exception as er:
            print('Ошибка при отправке API запроса:', er)
            time.sleep(10)
            continue

        # if fork_info['fork_id'] in AllBetsSet:
        #     print(f"Ставка {fork_info['fork_id']} уже проставлена!")
        #     time.sleep(10)
        #     continue
        AllBetsSet.add(fork_info['fork_id'])

        # проставление ставок на всех аккаунтах (Pool)
        try:
            print('-'*100)
            A = []
            for i in range(len(List_of_bet_account)):
                account_arr = [List_of_bet_account[i],
                               fork_info['sport_name'],
                                fork_info['bet365_href'],
                                fork_info['bet365_type'],
                                fork_info['bet365_coef']]
                A.append(account_arr)

            with Pool(processes=len(List_of_bet_account)) as p:
                p.map(make_bet_multipotok, A)
        except:
            print('Ошибка при проставлении ставок (Pool)')

        time.sleep(30)

    AllBetsSet = set()

    # Вывод текущего времени
    now = datetime.datetime.now()
    now = now.strftime('%H:%M:%S')
    print(now)

    # реанимация .com аккаунтов
    with Pool(processes=len(List_of_bet_account)) as p:
        A = [i for i in List_of_bet_account]
        p.map(reanimate_bet365com, A)

    # проверка, завис ли аккаунты
    with Pool(processes=len(List_of_bet_account)) as p:
        A = [i for i in List_of_bet_account]
        p.map(check_is_account_froze, A)

    if porezan_counter % 6 == 0:
        # предварительный поиск порезанных аккаунтов
        porezan_counter = 1
        try:
            with Pool(processes=len(List_of_bet_account)) as p:
                p.map(cheeck_porezan_li_account, List_of_bet_account)
        except Exception as er:
            print(er)
        i_porez = 0
        while i_porez < len(List_of_bet_account):
            if not List_of_bet_account[i_porez].is_valud_account:
                telegram_text = f'{List_of_bet_account[i_porez].bet365_login} - порезан. Баланс: {List_of_bet_account[i_porez].get_balance()} '
                telegram_notify1.telegram_bot_send_message(telegram_text)
                delete_account_from_txt_by_login(List_of_bet_account[i_porez].bet365_login)
                print(f'Аккаунт {List_of_bet_account[i_porez].bet365_login} - порезан')
                List_of_bet_account[i_porez].driver.quit()
                List_of_bet_account.pop(i_porez)
            else:
                i_porez += 1
        # завершение поиска порезанных аккаунтов
    else:
        porezan_counter += 1
    print(f'Осталось рабочих аккаунтов: {len(List_of_bet_account)}')





