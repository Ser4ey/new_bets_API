import random
import time
from selenium import webdriver
from multiprocessing.dummy import Pool
import data


def cool_decorator(method_to_decorate, type_of_account):
    def wrapper(url):
        if (type_of_account == 'RU') and ('bet365' in url):
            url = url.replace('.com', '.ru')
        return method_to_decorate(url)
    return wrapper


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
            except:
                return False

        def open_new_window_2ip(driver):
            current_window = driver.current_window_handle
            driver.execute_script(f"window.open('https://2ip.ru/', '_blank')")
            time.sleep(7)
            driver.switch_to.window(driver.window_handles[-1])
            # driver.close()
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
                    # driver.quit()
                    return driver, 'Сайт bet365 не загрузился'
            except:
                # driver.quit()
                return driver, 'Сайт bet365 не загрузился'

        def add_accounts_to_list(Browsers_List):
            time_to_sleep = random.randint(1, 1000) / 500
            time.sleep(time_to_sleep)
            driver, info = get_driver()
            if info == 'OK':
                Browsers_List.append(driver)
                print('+1 browser')
            else:
                print('+0 browser')

        # число браузеров, которое будет открыто за раз
        number_of_tries = 3
        Browser_List = []

        while len(Browser_List) < self.number_of_accounts:
            try:
                with Pool(processes=number_of_tries) as p:
                    p.map(add_accounts_to_list, [Browser_List for i in range(number_of_tries)])
            except Exception as er:
                print(f'Ошибка при выполнениии Poll: {er}')

            print('Проверка браузеров!')
            Browser_List_checked = []
            for i in range(len(Browser_List)):
                browser_ = Browser_List[i]
                if check_bet365(browser_):
                    print(f'{i} браузер - работает')
                    Browser_List_checked.append(browser_)
                else:
                    print(f'{i} браузер - не загрузился!')
                    # try:
                    #     browser_.close()
                    #     browser_.quit()
                    # except:
                    #     pass
            Browser_List = Browser_List_checked[:]

            print(f'Открыто {len(Browser_List)} из {self.number_of_accounts} аккаунтов')


        while len(Browser_List) > self.number_of_accounts:
            Browser_List.pop(-1).quit()
            print('1 лишний аккаунт удалён')

        self.Browser_List = Browser_List

    def return_Browser_List(self):
        return self.Browser_List


accounts_get_class = GetWorkAccountsList(number_of_accounts=3, vpn_country='UK')
Accounts = accounts_get_class.return_Browser_List()