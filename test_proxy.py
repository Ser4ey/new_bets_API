from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium import webdriver


def open_one_proxy_account():
    proxy = "51.89.191.226:10239"
    log_pass = 'avraint2305:01bbbe'

    firefox_profile = r'C:\Users\Sergey\AppData\Roaming\Mozilla\Firefox\Profiles\s5auea2f.default-release'
    firefox_binary = r'C:\Program Files\Mozilla Firefox\firefox.exe'
    path_to_geckodriver = r'C:\Users\Sergey\PycharmProjects\new_bets_API\geckodriver.exe'



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
