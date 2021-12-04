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
from selenium.webdriver.common.proxy import Proxy, ProxyType



class FireFoxDriverWithProxy:
    def __init__(self, proxy, bet_value='5'):

        self.is_VPN = True
        firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True

        print(proxy, sep='')

        proxy_host = proxy.split(':')[0]
        proxy_port = proxy.split(':')[1]
        print(proxy_host, proxy_port)

        fp = webdriver.FirefoxProfile()
        fp.set_preference("network.proxy.type", 1)
        fp.set_preference("network.proxy.http", proxy_host)
        fp.set_preference("network.proxy.http_port", proxy_port)
        fp.set_preference("network.proxy.https", proxy_host)
        fp.set_preference("network.proxy.https_port", proxy_port)
        fp.set_preference("network.proxy.ssl", proxy_host)
        fp.set_preference("network.proxy.ssl_port", proxy_port)
        fp.set_preference("network.proxy.ftp", proxy_host)
        fp.set_preference("network.proxy.ftp_port", proxy_port)
        fp.set_preference("network.proxy.socks", proxy_host)
        fp.set_preference("network.proxy.socks_port", proxy_port)


        # fp = webdriver.FirefoxProfile(data.firefox_profile_path)
        # fp = webdriver.FirefoxProfile()
        # fp.set_preference("browser.privatebrowsing.autostart", True)
        # fp.update_preferences()

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



d1 = FireFoxDriverWithProxy('78.157.219.235:10321')
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

