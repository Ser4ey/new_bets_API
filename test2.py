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
for i in range(1):
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

while True:
    input('enter pleas:')
    List_of_bet_account[0].restart_browser_and_bet365_account()