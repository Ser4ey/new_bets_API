from chromdriver_class import FireFoxDriverMain, FireFoxForPimatch
from data import AccountsBet365, path_to_accounts_file
import datetime
from multiprocessing.dummy import Pool
import time
import random
from telegram_API import telegram_notify1
from selenium import webdriver
import data


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
    driver, info = get_driver()
    print(info)
    if info == 'OK':
        List_of_Bet365_open.append(driver)
        print('+1 открытый сайт bet365')
    else:
        try:
            driver.close()
            driver.quit()
        except:
            pass


List_of_Bet365_open = []
list_of_start_info = []

i1 = 1
for i in range(len(AccountsBet365)):
    account_data = AccountsBet365[i]
    start_info = [account_data['bet365_login'], account_data['bet365_password'], account_data['bet_value']]
    list_of_start_info.append(start_info)
    i1 += 1


while len(List_of_Bet365_open) < len(list_of_start_info):
    with Pool(processes=len(list_of_start_info)) as p:
        p.map(add_accounts_to_list, [i for i in range(20)])

    print(f'Необходимо ещё открыть сайтов: {len(list_of_start_info) - len(List_of_Bet365_open)}')
    print(f'Уже аккаунтов открыто: {len(List_of_Bet365_open)}')


print(f'Numbers of accounts: {len(List_of_Bet365_open)}')
print(List_of_Bet365_open)
