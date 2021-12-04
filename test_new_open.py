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
            "ftpProxy": proxy,
            "sslProxy": proxy
        }


        fp = webdriver.FirefoxProfile(data.firefox_profile_path)
        # fp = webdriver.FirefoxProfile()
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

        input(f'Tab Enter:')

    def check_bet365(self):
        # провепка правильно ли открылся сайт bet365
        try:
            time.sleep(2)
            self.driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_LoginContainer')
            return True
        except Exception as er:
            # print(f'Сайт bet365 открыт не правильно: {er}')
            return False



d1 = FireFoxDriverWithProxy('78.157.219.235:10321', 'avraint2305:01bbbe')
print('go')
d1.driver.get('https://2ip.ru')

try:
    print('Bet365 open:')
    d1.driver.get('https://bet365.com')
    print(f'bet365 open - {time.time()}')
except Exception as er:
    print(er)

for i in range(1000):
    print(f'is valid {i}')
    if d1.check_bet365():
        break

print(f'end: {time.time()}')

