import pickle
import threading
import selenium
from selenium import webdriver
import time
import data
import random
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from multiprocessing.dummy import Pool


class FireFoxDriverWithProxy:
    def __init__(self, proxy, proxy_login_and_password, bet_value='5'):

        self.is_VPN = True
        firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True

        print(proxy, ':', proxy_login_and_password, sep='')
        firefox_capabilities['proxy'] = {
            "proxyType": "MANUAL",
            "httpProxy": proxy,
            # "ftpProxy": proxy,
            "sslProxy": proxy
        }

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

        self.driver = driver
        self.bet_value = bet_value

        if proxy_login_and_password == 'no_login_for_proxy':
            print('Вы используете прокси с привязкой к ip!')
        else:
            print(f'Введите логин и пароль от прокси - {proxy_login_and_password}')
            input('Затем нажмите Enter:')


d1 = FireFoxDriverWithProxy('185.173.39.119:8245', 'abramyanpr:abramyanpr')
d1.driver.get('https://2ip.ru')
print('Bet365 open:')
d1.driver.get('https://bet365.com')


