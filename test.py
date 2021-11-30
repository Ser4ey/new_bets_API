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


def cool_decorator(method_to_decorate, type_of_account):
    def wrapper(url):
        if (type_of_account == 'RU') and ('bet365' in url):
            url = url.replace('.com', '.ru')
        return method_to_decorate(url)
    return wrapper


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

driver.get = cool_decorator(driver.get, 'RU')

driver.get('https://google.com')
time.sleep(10)
driver.get('https://bet365.com')






