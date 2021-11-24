from chromdriver_class import FireFoxDriverMainNoAutoOpen, FireFoxForPimatch
from data import AccountsBet365, path_to_accounts_file
import datetime
from multiprocessing.dummy import Pool
import time
from telegram_API import telegram_notify1
from selenium import webdriver
import data
from API_worker import APIWorker1
import random

# needed f
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

# needed f
def open_new_window_2ip(driver):
    current_window = driver.current_window_handle
    driver.execute_script(f"window.open('https://2ip.ru/', '_blank')")
    time.sleep(7)
    driver.switch_to.window(driver.window_handles[-1])
    driver.close()
    driver.switch_to.window(current_window)


def check_bet365(driver):
    # провепка правильно ли открылся сайт bet365
    try:
        time.sleep(2)
        driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_LoginContainer')
        return True
    except Exception as er:
        print(f'Сайт bet365 открыт не правильно: {er}')
        return False


def get_driver():
    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True

    fp = webdriver.FirefoxProfile(data.firefox_profile_path)
    fp.set_preference("browser.privatebrowsing.autostart", True)

    options = webdriver.FirefoxOptions()
    options.add_argument("-private")
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("dom.webnotifications.enabled", False)
    binary = data.firefox_binary
    options.binary = binary

    driver = webdriver.Firefox(capabilities=firefox_capabilities, firefox_profile=fp,
                               firefox_binary=data.firefox_binary,
                               executable_path=data.path_to_geckodriver,
                               options=options)

    time.sleep(10)
    driver.get('https://2ip.ru/')
    driver.set_page_load_timeout(15)
    try:
        driver.get('https://www.bet365.com/')
        driver.set_page_load_timeout(25)
        if check_bet365(driver):
            return driver, 'OK'
    except:
        pass

    driver.set_page_load_timeout(25)
    for i in range(2):
        open_new_window_2ip(driver)
        time.sleep(0.3)

    try:
        driver.get('https://www.bet365.com/')
        if check_bet365(driver):
            return driver, 'OK'
        else:
            return driver, 'Сайт bet365 не загрузился'
    except:
        return driver, 'Сайт bet365 не загрузился'


def add_accounts_to_list(a=''):
    global List_of_Bet365_open
    # задержка
    time_to_sleep = random.randint(1, 1000) / 500
    time.sleep(time_to_sleep)
    print(f'start: {a}')
    driver, info = get_driver()
    if info == 'OK':
        List_of_Bet365_open.append(driver)
        print('+1 открытый сайт bet365')
    else:
        try:
            driver.close()
            driver.quit()
        except:
            pass
    print(f'end: {a}')


def log_in_driver(driver_class):
    login = driver_class.bet365_login
    passwd = driver_class.bet365_password
    driver_class.log_in_bet365_v2(login, passwd)


driverParimatch = FireFoxForPimatch()

List_of_Bet365_open = []
list_of_start_info = []

i1 = 1
# for i in range(len(AccountsBet365)):
for i in range(4):
    account_data = AccountsBet365[i]
    start_info = [account_data['bet365_login'], account_data['bet365_password'], account_data['bet_value']]
    list_of_start_info.append(start_info)
    i1 += 1

numbers_of_processes = 8
while True:
    try:
        with Pool(processes=numbers_of_processes) as p:
            p.map(add_accounts_to_list, [i for i in range(numbers_of_processes)])
    except Exception as er:
        print(f'Ошибка при выполнениии Poll: {er}')

    print(f'Необходимо ещё открыть сайтов: {len(list_of_start_info) - len(List_of_Bet365_open)} из {len(list_of_start_info)}')
    if (len(list_of_start_info) - len(List_of_Bet365_open)) < 1:
        print('Все аккаунты загружены')
        break

# удаление избыточсных аккаунтов
while len(List_of_Bet365_open) > len(list_of_start_info):
    List_of_Bet365_open[-1].quit()
    List_of_Bet365_open.pop(-1)
    print('1 лишний аккаунт удалён')


List_of_bet_account = []
for i in range(len(list_of_start_info)):
    driver_class = FireFoxDriverMainNoAutoOpen(
        driver=List_of_Bet365_open[i],
        login=list_of_start_info[i][0],
        password=list_of_start_info[i][1],
        bet_value=list_of_start_info[i][2]
    )

    List_of_bet_account.append(driver_class)

# авторизация аккаунтов
with Pool(processes=numbers_of_processes) as p:
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

        if fork_info['fork_id'] in AllBetsSet:
            print(f"Ставка {fork_info['fork_id']} уже проставлена!")
            time.sleep(10)
            continue
        AllBetsSet.add(fork_info['fork_id'])

        try:
            second_coef = driverParimatch.find_coef_for_any_sport(fork_info['sport_name'], fork_info['parimatch_href'], fork_info['parimatch_type'])
            print(f'Коэффициент на париматч: {second_coef}')
            try:
                float(second_coef)
            except:
                print('Ставка не поддерживается')
                continue
            if float(second_coef) + 0.05 < float(fork_info['parimatch_coef']):
                print('Коэффициет на париматч упал!', f'{fork_info["parimatch_coef"]} -> {second_coef}')
                continue
        except:
            print('Не удалось получить коэффициент для париматч')
            continue

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





