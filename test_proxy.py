from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium import webdriver
import data

def open_one_proxy_account():
    proxy = "51.89.191.226:10239"
    log_pass = 'avraint2305:01bbbe'

    firefox_profile = data.firefox_profile_path
    firefox_binary = data.firefox_binary
    path_to_geckodriver = data.path_to_geckodriver



    firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    firefox_capabilities['marionette'] = True

    firefox_capabilities['proxy'] = {
        "proxyType": "MANUAL",
        "httpProxy": proxy,
        "sslProxy": proxy
    }

    fp = webdriver.FirefoxProfile(firefox_profile)
    fp.set_preference("browser.privatebrowsing.autostart", True)

    options = webdriver.FirefoxOptions()
    options.add_argument("-private")
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("dom.webnotifications.enabled", False)
    binary = firefox_binary
    options.binary = binary


    driver = webdriver.Firefox(capabilities=firefox_capabilities, firefox_profile=fp,
                               firefox_binary=firefox_binary,
                               executable_path=path_to_geckodriver,
                               options=options)


    driver.get('https://2ip.ru')
    input(f'Введите: {log_pass}')

    driver.get('https://bet365.com')

    return driver
