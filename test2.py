import random
import time
from selenium import webdriver
from multiprocessing.dummy import Pool
import data
from chromdriver_class import FireFoxDriverMainNoAutoOpen
from data import AccountsBet365, path_to_accounts_file


def cool_decorator(method_to_decorate, type_of_account):
    def wrapper(url):
        if (type_of_account == 'RU') and ('bet365' in url):
            url = url.replace('.com', '.ru')
        return method_to_decorate(url)
    return wrapper

def log_in_driver(driver_class):
    login = driver_class.bet365_login
    passwd = driver_class.bet365_password
    driver_class.log_in_bet365_v2(login, passwd)


class GetWorkAccountsList:
    def __init__(self, number_of_accounts, vpn_country):
        self.firefox_profile = data.VPN_dict['UK']
        # какое VPN, профиль и ссылки
        self.vpn_country = vpn_country
        self.ru_account = False
        if self.vpn_country == 'RU':
            self.ru_account = True
            self.firefox_profile = data.VPN_dict['RU']
        elif self.vpn_country == 'UK':
            self.firefox_profile = data.VPN_dict['UK']
        elif self.vpn_country == 'CH':
            self.firefox_profile = data.VPN_dict['CH']

        self.number_of_accounts = number_of_accounts

        def check_bet365(driver):
            # провепка правильно ли открылся сайт bet365
            try:
                time.sleep(2)
                driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_LoginContainer')
                return True
            except Exception as er:
                return False

        def open_new_window_2ip(driver):
            current_window = driver.current_window_handle
            driver.execute_script(f"window.open('https://2ip.ru/', '_blank')")
            time.sleep(7)
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
            driver.switch_to.window(current_window)

        def get_driver():
            firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
            firefox_capabilities['marionette'] = True

            fp = webdriver.FirefoxProfile(self.firefox_profile)
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

            driver.get = cool_decorator(driver.get, self.vpn_country)
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

        def add_accounts_to_list(Browsers_List=[]):
            # задержка
            time_to_sleep = random.randint(1, 1000) / 500
            time.sleep(time_to_sleep)
            driver, info = get_driver()
            if info == 'OK':
                Browsers_List.append(driver)
                print('+1 browser')
            else:
                try:
                    driver.close()
                    driver.quit()
                except:
                    pass

        # число браузеров, которое будет открыто
        number_of_tries = 6
        Browser_List = []

        while len(Browser_List) < self.number_of_accounts:
            try:
                with Pool(processes=number_of_tries) as p:
                    p.map(add_accounts_to_list, [Browser_List for i in range(number_of_tries)])
            except Exception as er:
                print(f'Ошибка при выполнениии Poll: {er}')
            print(f'Открыто {len(Browser_List)} из {self.number_of_accounts} аккаунтов')


        while len(Browser_List) > self.number_of_accounts:
            Browser_List.pop(-1).quit()
            print('1 лишний аккаунт удалён')

        self.Browser_List = Browser_List

    def return_Browser_List(self):
        return self.Browser_List

List_of_Bet365_open = []
list_of_start_info = []

i1 = 1
for i in range(len(AccountsBet365)):
    account_data = AccountsBet365[i]
    start_info = [account_data['bet365_login'], account_data['bet365_password'], account_data['bet_value'], account_data['vpn_country']]
    list_of_start_info.append(start_info)
    i1 += 1

List_of_bet_account = []

accounts_get_class = GetWorkAccountsList(number_of_accounts=1, vpn_country='UK')
Accounts = accounts_get_class.return_Browser_List()


print(f'Все аккаунты успешно авторизованы!')

for account_info in list_of_start_info[:1]:
    bet365login, bet365password, bet_value, vpn_country = account_info

    driver_class = FireFoxDriverMainNoAutoOpen(
        driver=Accounts.pop(-1),
        login=bet365login,
        password=bet365password,
        bet_value=bet_value,
        vpn_country=vpn_country
    )

    List_of_bet_account.append(driver_class)

with Pool(processes=len(List_of_bet_account)) as p:
    p.map(log_in_driver, List_of_bet_account)
account1 = List_of_bet_account[0]

while True:
    url = input('url:')
    bet_type = input('bet_type:')
    coef = input('coef:')

    account1.make_cyber_football_bet(url, bet_type, coef)

    input(':::')
    account1.close_cupon2()