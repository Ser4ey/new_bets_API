import pickle
import threading
import selenium
from selenium import webdriver
import time
import data
import random
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


class FireFoxDriverMain:
    def __init__(self, bet_value):
        self.is_VPN = True
        # аккаунт рабочий, если значение меняется на False, то аккаунт закрывается
        self.is_valud_account = True
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

        self.driver = driver
        self.bet_value = bet_value

    def restart_driver(self):
        try:
            self.driver.close()
            self.driver.quit()
        except:
            pass

        self.is_VPN = True
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

        self.driver = driver

    def open_bet365com(self):
        time.sleep(10)
        self.driver.get('https://2ip.ru/')
        self.driver.set_page_load_timeout(10)
        try:
            self.driver.get('https://www.bet365.com/')
            return None
        except:
            pass

        for i in range(7):
            self.open_new_window_2ip()
            time.sleep(1)

        self.driver.set_page_load_timeout(75)

        try:
            self.driver.get('https://www.bet365.com/')
        except:
            print('Сайт bet365 не загрузился')
            return 'Сайт bet365 не загрузился'

    def open_new_window_2ip(self):
        current_window = self.driver.current_window_handle
        self.driver.execute_script(f"window.open('https://2ip.ru/', '_blank')")
        time.sleep(7)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.close()
        self.driver.switch_to.window(current_window)

    def log_in_bet365(self, login, password):
        self.bet365_login = login
        self.bet365_password = password

        try:
            self.driver.get('https://www.bet365.com/')
        except:
            pass

        for i in range(10):
            try:
                try:
                    time.sleep(5)
                    self.driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_LoginContainer')
                    break
                except:
                    print('refresh')
                    self.driver.get('https://www.bet365.com/')
                    print('-')
            except:
                pass

        print(f'Вход в аккаунт: {login}')
        time.sleep(5)
        # вход в аккаунт bet365ru
        for i in range(10):
            try:
                self.driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_LoginContainer').click()
                break
            except:
                print(f'Не удалось войти в аккаунт {login}!')
                time.sleep(2)

        time.sleep(5)
        for i in range(10):
            try:
                self.driver.find_element_by_class_name('lms-StandardLogin_Username').send_keys(login)
                time.sleep(0.7)
                self.driver.find_element_by_class_name('lms-StandardLogin_Password').send_keys(password)
                time.sleep(0.7)
                break
            except:
                time.sleep(1)
                print(f'Не удалось войти в аккаунт {login}')
                return

        self.driver.find_element_by_class_name('lms-StandardLogin_LoginButton').click()
        time.sleep(15)
        self.bet365_account_name = login

        # закрываем окно с почтой
        try:
            time.sleep(3)
            frame = self.driver.find_element_by_class_name('lp-UserNotificationsPopup_Frame')
            self.driver.switch_to.frame(frame)
            # print('open page')
            self.driver.find_element_by_id('RemindMeLater').click()
        except Exception as er:
            # print(er)
            pass
        finally:
            self.driver.switch_to.default_content()

        try:
            time.sleep(5)
            self.driver.find_element_by_class_name('pm-PushTargetedMessageOverlay_CloseButton ').click()
        except:
            pass

        print(f'Вы успешно вошли в аккаунт {login}')

    def relogin_in_bet365_if_take_off(self):
        try:
            self.driver.get('https://www.bet365.com/')
        except:
            pass
        time.sleep(5)
        try:
            self.driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_LoginContainer')
            print(f'Аккаунт {self.bet365_login} вылетел!')
        except:
            print(f'Аккаунт {self.bet365_login} авторизован')
            return f'Аккаунт {self.bet365_login} авторизован'

        print(f'Повторный вход в аккаунт: {self.bet365_login}')

        for i in range(10):
            try:
                self.driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_LoginContainer').click()
                break
            except:
                print(f'Не удалось войти в аккаунт {self.bet365_login}!')
                time.sleep(2)

        time.sleep(5)
        for i in range(10):
            try:
                self.driver.find_element_by_class_name('lms-StandardLogin_Username').clear()
                time.sleep(0.7)
                self.driver.find_element_by_class_name('lms-StandardLogin_Username').send_keys(self.bet365_login)
                time.sleep(0.7)
                self.driver.find_element_by_class_name('lms-StandardLogin_Password').send_keys(self.bet365_password)
                time.sleep(0.7)
                break
            except:
                time.sleep(1)
                print(f'Не удалось войти в аккаунт {self.bet365_login}')
                return

        self.driver.find_element_by_class_name('lms-StandardLogin_LoginButton').click()
        time.sleep(15)

        # закрываем окно с почтой
        try:
            time.sleep(3)
            frame = self.driver.find_element_by_class_name('lp-UserNotificationsPopup_Frame')
            self.driver.switch_to.frame(frame)
            # print('open page')
            self.driver.find_element_by_id('RemindMeLater').click()
        except Exception as er:
            # print(er)
            pass
        finally:
            self.driver.switch_to.default_content()

        try:
            time.sleep(5)
            self.driver.find_element_by_class_name('pm-PushTargetedMessageOverlay_CloseButton ').click()
        except:
            pass

        print(f'Вы успешно перевошли в аккаунт {self.bet365_login}')
        return f'Вы успешно перевошли в аккаунт {self.bet365_login}'

    def get_balance(self):
        try:
            bet365balance = self.driver.find_element_by_class_name('hm-MainHeaderMembersWide_Balance').text
            return bet365balance
        except:
            return 'Не удалось получить баланс аккаунта'

    def make_a_bet(self, value, coef, element):
        '''Ставит ставку в открывшемся окошечке
        (его нужно предварительно открыть)'''

        time.sleep(1)

        if str(value)[0] == '%':
            value = value[1:]
            value = float(value)
            value = value / 100
            try:
                bet365balance = self.driver.find_element_by_class_name('hm-MainHeaderMembersWide_Balance').text
                bet365balance = bet365balance.split(',')[0]
                bet365balance = bet365balance.strip()
                bet365balance = bet365balance.strip('£')
                bet365balance = bet365balance.replace(' ', '')
                bet365balance = float(bet365balance)
                print(f'Баланс аккаунта {bet365balance}')
            except:
                bet365balance = 10
                print(f'Баланс аккаунта {bet365balance} не найден')

            print(f'bet = {bet365balance} * {value}')
            value = bet365balance * value
            value = round(value, 2)
            print('value:', value)

        coef_now = self.driver.find_element_by_class_name('bsc-OddsDropdownLabel').text
        coef_now = float(coef_now)
        print(f'Текущий коэффициент - {coef_now} Нужный коэффициент - {coef}')
        coef = float(coef)
        if coef - coef_now > 0.09:
            print('Коэффициэнт сильно изменился')
            time.sleep(1)
            element.click()
            self.driver.get('https://www.bet365.com/')
            time.sleep(2)
            return

        self.driver.find_element_by_class_name('qbs-NormalBetItem_DetailsContainer ') \
            .find_element_by_class_name('qbs-StakeBox_StakeInput ').click()
        time.sleep(0.3)
        for simvol in str(value):
            self.driver.find_element_by_tag_name("body").send_keys(simvol)
            time.sleep(0.3)
        time.sleep(0.5)
        try:
            # нажимаем на кнопку стандартной ставки
            self.driver.find_element_by_class_name('qbs-BetPlacement ').click()
        except:
            # нажимаем на кнопку ставки, которую нужно одобрить
            self.driver.find_element_by_class_name('qbs-PlaceBetReferButton ').click()

        flag = False

        for i in range(15):
            try:
                self.driver.find_element_by_class_name('qbs-QuickBetHeader_DoneButton ').click()
                print('Ставка проставлена!')
                return 'Ставка проставлена!'
            except:
                time.sleep(1)

        print('[-] Не удалось поставить ставку')
        try:
            self.driver.find_element_by_class_name('qbs-NormalBetItem_Indicator ').click()
        except:
            pass

        self.driver.get('https://www.bet365.com/#/HO/')

        time.sleep(2)

    def reanimaite_bet365com(self):
        # попытка закрыть купон
        try:
            self.driver.find_element_by_class_name('qbs-NormalBetItem_Indicator ').click()
            time.sleep(2)
        except:
            pass

        # попытка закрыть уведомление о сообщениях
        try:
            self.driver.find_element_by_class_name('pm-PushTargetedMessageOverlay_CloseButton ').click()
            time.sleep(2)
        except:
            pass

        # попытка закрыть окно неактивности
        try:
            self.driver.get('https://www.bet365.com/')
            time.sleep(3)
            self.driver.find_element_by_class_name('alm-ActivityLimitAlert_Button ').click()
        except:
            pass

        self.close_cupon()

        self.relogin_in_bet365_if_take_off()

    def close_cupon(self):
        '''Попытка Закрытие купонов(а_ если он есть)'''
        try:
            #open_cupon
            self.driver.find_element_by_class_name('bss-StandardHeader ').click()
            time.sleep(4)
            #очистка купона
            self.driver.find_element_by_class_name('bs-ControlBar_RemoveButton ').click()
            time.sleep(4)
        except Exception as er:
            print('нет купонов', er)

    def check_is_account_not_valid_mean_porezan(self):
        '''Провепка порезан ли аккаунт'''
        self.driver.get('https://www.bet365.com/#/ME/X6500')
        time.sleep(10)

        iframe1 = self.driver.find_element_by_id('MembersIframe')
        self.driver.switch_to.frame(iframe1)
        time.sleep(0.5)
        iframe2 = self.driver.find_element_by_id('MembersHostFrame')
        self.driver.switch_to.frame(iframe2)

        messages_blocks = self.driver.find_elements_by_class_name('details')

        for block_ in messages_blocks:
            title_text = block_.find_element_by_tag_name('span').text
            if title_text == 'Ваша учётная запись':
                self.is_valud_account = False
                self.driver.switch_to.default_content()
                return True

        self.driver.switch_to.default_content()
        return False


    def make_cyber_football_bet(self, url, bet_type, coef):
        bet_value = self.bet_value

        # WIN__P1 | WIN__P2 | WIN__PX
        if bet_type == 'WIN__P1' or bet_type == 'WIN__P2' or bet_type == 'WIN__PX':
            self.make_cyber_football_bet_P1_P2_X(url, bet_type, coef, bet_value)
        elif bet_type == 'WIN__1X' or bet_type == 'WIN__X2' or bet_type == 'WIN__12':
            self.make_cyber_football_bet_double_chance_P1X_XP2_P1P2(url, bet_type, coef, bet_value)
        elif bet_type[:13] == 'TOTALS__UNDER' or bet_type[:12] == 'TOTALS__OVER':
            self.make_cyber_football_bet_totalbet_of_game(url, bet_type, coef, bet_value)
        elif bet_type[:10] == 'P1__TOTALS' or bet_type[:10] == 'P2__TOTALS':
            self.make_cyber_football_bet_totalbet_of_teme_1or2(url, bet_type, coef, bet_value)
        else:
            print('This type not supported now!')

        '''

        elif bet_type[:13] == 'Гола не будет':
            self.make_cyber_football_bet_gola_ne_budet(url, bet_type, coef, bet_value)
        elif bet_type == 'Чет' or bet_type == 'Нечет':
            self.make_cyber_football_bet_odd_or_even(url, bet_type, coef, bet_value)
        elif 'Г1' in bet_type or 'Г2' in bet_type:
            self.make_cyber_football_bet_gandikap_with_3_exists(url, bet_type, coef, bet_value)
        elif 'Ф1' in bet_type or 'Ф2' in bet_type:
            self.make_cyber_football_bet_F1_F2(url, bet_type, coef, bet_value)
        else:
            if 'Команда' in bet_type:
                if 'Тб' in bet_type or 'Тм' in bet_type:
                    self.make_cyber_football_bet_totalbet_of_teme_1or2(url, bet_type, coef, bet_value)
                    return
            if 'Тб' in bet_type or 'Тм' in bet_type:
                self.make_cyber_football_bet_totalbet_of_game(url, bet_type, coef, bet_value)
                return

            print('Неизвестный тип ставки')'''

    def make_cyber_football_bet_P1_P2_X(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку(Победа|Ничья|Поражение) url: {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')

        bet_element = list_of_bets[0]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if (text != 'Результат основного времени') and (text != 'Fulltime Result'):
            print('Ставка на П1П2Х, указана колонка не результат основного времени!')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            bet_element.click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[0]


        element_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        bets = element_with_bets.find_elements_by_class_name('gl-Participant ')

        my_bet_number = 2
        if bet_type == 'WIN__P1':
            my_bet_number = 0
        elif bet_type == 'WIN__P2':
            my_bet_number = -1
        elif bet_type == 'WIN__PX':
            my_bet_number = 1
        else:
            print('Ставка на П1П2Х, неизвестный формат ставки')
            return 'Ставка на П1П2Х, неизвестный формат ставки'

        bets[my_bet_number].click()
        time.sleep(2)
        self.make_a_bet(bet_value, coef, bets[my_bet_number])

    def make_cyber_football_bet_double_chance_P1X_XP2_P1P2(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку(Двойной шанс) url: {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if (text1 == 'Двойной шанс') or (text1 == 'Double Chance'):
                line = i
                print('Ставка двойной шанс найдена')
                break

        bet_element = list_of_bets[line]

        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if (text != 'Двойной шанс') and (text != 'Double Chance'):
            print('Ставка(Двойной шанс) не найдена')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        element_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        bets = element_with_bets.find_elements_by_class_name('gl-Participant ')

        my_bet_number = 2
        if bet_type == 'WIN__1X':
            my_bet_number = 0
        elif bet_type == 'WIN__X2':
            my_bet_number = 1
        elif bet_type == 'WIN__12':
            my_bet_number = -1
        else:
            print('Ставка на (Двойной шанс) , неизвестный формат ставки')
            return 'Ставка на (Двойной шанс) , неизвестный формат ставки'

        bets[my_bet_number].click()
        time.sleep(2)
        self.make_a_bet(bet_value, coef, bets[my_bet_number])

    def make_cyber_football_bet_totalbet_of_game(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку total bet url: {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if (text1 == 'Голы матча') or (text1 == 'Match Goals'):
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if (text != 'Голы матча') and (text != 'Match Goals'):
            print('Ставка(Голы матча не найдена/total bet) не найдена')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        element_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')

        goul_count = element_with_bets.find_element_by_class_name('srb-ParticipantLabelCentered_Name ').text
        bets = element_with_bets.find_elements_by_class_name('gl-ParticipantOddsOnly ')

        number_of_gouls = bet_type.split('(')
        number_of_gouls = number_of_gouls[-1]
        number_of_gouls = number_of_gouls.strip(')')
        number_of_gouls = number_of_gouls.strip('')

        if number_of_gouls != goul_count:
            print(f'Число голов не совпадает {goul_count}|{number_of_gouls}')
            return

        if 'OVER' in bet_type:
            bets[0].click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bets[0])
        else:
            bets[1].click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bets[1])

    def make_cyber_football_bet_totalbet_of_teme_1or2(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку total bet team url: {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 'None'
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text[-4:]
            text1_2 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if (text1 == 'ГОЛЫ') or (text1 == 'oals' and len(text1_2) > 12):
                line = i
                print(f'line: {line}')
                break

        if line == 'None':
            print('Total bet на команду не найдена')
            return

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if 'P2' in bet_type:
            line += 1
            bet_element = list_of_bets[line]

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        element_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')

        goul_count = element_with_bets.find_element_by_class_name('srb-ParticipantLabelCentered_Name ').text
        bets = element_with_bets.find_elements_by_class_name('gl-ParticipantOddsOnly ')

        bet_type = bet_type.strip(')')
        bet_type = bet_type.split('(')
        number_of_gouls = bet_type[1]
        bet_type = bet_type[0]

        if number_of_gouls != goul_count:
            print(f'Число голов не совпадает {goul_count}|{number_of_gouls}')
            return

        bet_element_1 = bets[0]
        if 'OVER' in bet_type:
            bets[0].click()
        else:
            bets[1].click()
            bet_element_1 = bets[1]

        time.sleep(2)
        self.make_a_bet(bet_value, coef, bet_element_1)

    def make_cyber_football_bet_gola_ne_budet(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку Гола не будет url: {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if text1[1:] == '-й Гол':
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if text[1:] != '-й Гол':
            print('Ставка(Двойной шанс) не найдена')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        element_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        bets = element_with_bets.find_elements_by_class_name('gl-Participant_General ')

        #gl-Participant_General
        my_bet_number = 1

        bets[my_bet_number].click()
        time.sleep(2)
        self.make_a_bet(bet_value, coef, bets[my_bet_number])

    def make_cyber_football_bet_odd_or_even(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку ЧетНечет: {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if text1 == 'Голы нечет/чёт':
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if text != 'Голы нечет/чёт':
            print('Ставка(Голы нечет/чёт) не найдена')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        element_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')


        bets = element_with_bets.find_elements_by_class_name('gl-Market_General-cn2 ')

        if bet_type == 'Чет':
            bets[1].click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bets[1])
        else:
            bets[0].click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bets[0])

    def make_cyber_football_bet_gandikap_with_3_exists(self, url, bet_type, coef, bet_value):
        # Г1(1) Г2(0) Г1(-1)   (1 -> +1)
        print(f'Проставляем ставку Гандикап с 3 исходами url: {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if text1 == 'ГАНДИКАП С 3 ИСХОДАМИ':
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if text != 'ГАНДИКАП С 3 ИСХОДАМИ':
            print('Ставка Гандикап с 3 исходами не найдена')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        element_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')

        gandicaps = element_with_bets.find_elements_by_class_name('gl-ParticipantCentered_Handicap')
        bets_list = element_with_bets.find_elements_by_class_name('gl-ParticipantCentered ')

        true_gandicap = bet_type[3:]
        true_gandicap = true_gandicap.strip('(')
        true_gandicap = true_gandicap.strip(')')

        if true_gandicap == '0':
            pass
        elif true_gandicap[0] == '-':
            pass
        else:
            true_gandicap = '+' + true_gandicap

        print(f'true gandicap: {true_gandicap}')

        if 'Г1' in bet_type:
            line_ = 0
        else:
            line_ = -1

        gandicap = gandicaps[line_]
        bet_ = bets_list[line_]

        if gandicap != true_gandicap:
            print('Гандикап изменился')
            return

        bet_.click()
        time.sleep(2)
        self.make_a_bet(bet_value, coef, bet_)

    def make_cyber_football_bet_F1_F2(self, url, bet_type, coef, bet_value):
        # Ф2(-3)
        print(f'Проставляем ставку Ф url: {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if 'АЗИАТСКИЙ ГАНДИКАП' in text1:
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if not 'АЗИАТСКИЙ ГАНДИКАП' in text:
            print('Ставка Ф не найдена')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        element_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')


        bets_list = element_with_bets.find_elements_by_class_name('gl-ParticipantCentered ')


        if 'Ф1' in bet_type:
            line_ = 0
        else:
            line_ = -1

        bet_ = bets_list[line_]

        bet_.click()
        time.sleep(2)
        self.make_a_bet(bet_value, coef, bet_)


    def make_table_tennis_bet(self, url, bet_type, coef, bet_value):
        '''Ставка на настольный теннис'''

        if bet_type == 'П1' or bet_type == 'П2':
            # П1 П2
            self.make_table_tennis_bet_P1_P2(url, bet_type, coef, bet_value)
        elif ('П1' in bet_type or 'П2' in bet_type) and len(bet_type) > 5:
            # П1 (1 партия)
            self.make_table_tennis_bet_P1_P2_of_game1(url, bet_type, coef, bet_value)
        elif ('Ф1' in bet_type or 'Ф2' in bet_type) and len(bet_type) < 10:
            # Ф1(-2.5)  Ф2(1.5)
            self.make_table_tennis_bet_F1_F2_gandikap_of_match(url, bet_type, coef, bet_value)
        elif ('Ф1' in bet_type or 'Ф2' in bet_type) and len(bet_type) > 10:
            # Ф1(-2.5) (3 партия)     Ф2(1.5) (1 партия)
            self.make_table_tennis_bet_F1_F2_gandikap_of_game1(url, bet_type, coef, bet_value)
        else:
            print('Неизвестный тип ставки (1)', bet_type)


    def make_table_tennis_bet_P1_P2(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку П1П2(table tennis): {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if text1 == 'ЛИНИИ МАТЧА':
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if text != 'ЛИНИИ МАТЧА':
            print('Ставка П1П2 настольный теннис')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        bet_text = columns_[0].find_elements_by_tag_name('div')[1].text
        if bet_text != 'Победитель':
            print('Не удалось найти ставку на победу (теннис)')
            return

        bet1 = columns_[1].find_elements_by_tag_name('div')[1]
        bet2 = columns_[2].find_elements_by_tag_name('div')[1]

        if bet_type == 'П1':
            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)

    def make_table_tennis_bet_P1_P2_of_game1(self, url, bet_type, coef, bet_value):
        '''Побеа в отдельной игре, а не на всю партию целиком'''

        print(f'Проставляем ставку П1 (3 партия)(table tennis): {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text
            # ИГРА 5 - ЛИНИИ
            if ('ИГРА' in text1) and ('ЛИНИИ' in text1):
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if not (('ИГРА' in text) and ('ЛИНИИ' in text)):
            print('Ставка П1 на игру матча?')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        line_ = -1
        # Гандикап (Игры)
        counter_ = 0
        for bet_text1 in columns_[0].find_elements_by_tag_name('div'):
            try:
                bet_text = bet_text1.text
                print(f'{counter_}: {bet_text}')
                if bet_text == 'Победитель':
                    line_ = counter_
                    # -1 ?
                    print(line_)
                    break
            except:
                pass
            counter_ += 1
        # bet_text = columns_[0].find_elements_by_tag_name('div')[1].text

        if line_ == -1:
            print('Не удалось найти ставку на Победу на игру (теннис)')
            return

        # srb-ParticipantCenteredStackedMarketRow_Handicap

        bet1 = columns_[1].find_elements_by_tag_name('div')[line_]
        bet2 = columns_[2].find_elements_by_tag_name('div')[line_]

        if 'П1' in bet_type:
            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)


    def make_table_tennis_bet_F1_F2_gandikap_of_match(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку Ф1(2.5)(Гандикап) (table tennis): {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')

        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if text1 == 'ЛИНИИ МАТЧА':
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if text != 'ЛИНИИ МАТЧА':
            print('Ставка Гандикап на матч?')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        line_ = -1
        # Гандикап (Игры)
        counter_ = 0
        for bet_text1 in columns_[0].find_elements_by_tag_name('div'):
            try:
                bet_text = bet_text1.text
                print(f'{counter_}: {bet_text}')
                if bet_text == 'Гандикап (Игры)':
                    line_ = counter_ - 1
                    #
                    print(line_)
                    break
            except:
                pass
            counter_ += 1
        # bet_text = columns_[0].find_elements_by_tag_name('div')[1].text

        if line_ == -1:
            print('Не удалось найти ставку на гандикап (теннис)')
            return

        # srb-ParticipantCenteredStackedMarketRow_Handicap

        bet1 = columns_[1].find_elements_by_tag_name('div')[line_]
        bet2 = columns_[2].find_elements_by_tag_name('div')[line_]

        bet1_gendikap_value = bet1.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text
        bet2_gendikap_value = bet2.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text
        print(f'1 gandicap: {bet1_gendikap_value}')
        print(f'2 gandicap: {bet2_gendikap_value}')

        true_gendikap_value = bet_type.split('(')
        true_gendikap_value = true_gendikap_value[-1]
        true_gendikap_value = true_gendikap_value.strip(')')
        if true_gendikap_value[0] != '-':
            true_gendikap_value = '+' + true_gendikap_value

        print(f'True gandicap: {true_gendikap_value}')

        if 'Ф1' in bet_type:
            if true_gendikap_value != bet1_gendikap_value:
                print('Значение гандикапа изменилось')
                return

            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            if true_gendikap_value != bet2_gendikap_value:
                print('Значение гандикапа изменилось')
                return

            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)


    def make_table_tennis_bet_F1_F2_gandikap_of_game1(self, url, bet_type, coef, bet_value):
        '''Гандикап на отдельную игру, а не на всё партию целиком'''

        print(f'Проставляем ставку Ф1(2.5) (3 партия) (Гандикап) (table tennis): {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text
            # ИГРА 5 - ЛИНИИ
            if ('ИГРА' in text1) and ('ЛИНИИ' in text1):
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if not (('ИГРА' in text) and ('ЛИНИИ' in text)):
            print('Ставка Гандикап на игру матча?')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        line_ = -1
        # Гандикап (Игры)
        counter_ = 0
        for bet_text1 in columns_[0].find_elements_by_tag_name('div'):
            try:
                bet_text = bet_text1.text
                print(f'{counter_}: {bet_text}')
                if bet_text == 'Гандикап':
                    line_ = counter_ - 1
                    # -1 ?
                    print(line_)
                    break
            except:
                pass
            counter_ += 1
        # bet_text = columns_[0].find_elements_by_tag_name('div')[1].text

        if line_ == -1:
            print('Не удалось найти ставку на гандикап на игру (теннис)')
            return

        # srb-ParticipantCenteredStackedMarketRow_Handicap

        bet1 = columns_[1].find_elements_by_tag_name('div')[line_]
        bet2 = columns_[2].find_elements_by_tag_name('div')[line_]

        bet1_gendikap_value = bet1.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text
        bet2_gendikap_value = bet2.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text

        true_gendikap_value = bet_type.split(' ')[0]
        true_gendikap_value = true_gendikap_value.split('(')
        true_gendikap_value = true_gendikap_value[-1]
        true_gendikap_value = true_gendikap_value.strip(')')
        if true_gendikap_value[0] != '-':
            true_gendikap_value = '+' + true_gendikap_value

        print(f'True gandicap: {true_gendikap_value}')

        if 'Ф1' in bet_type:
            if true_gendikap_value != bet1_gendikap_value:
                print('Значение гандикапа изменилось')
                return

            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            if true_gendikap_value != bet2_gendikap_value:
                print('Значение гандикапа изменилось')
                return

            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)


    def get_bet365_balance(self):
        url = 'https://www.bet365.ru/'
        if self.type_of_account == '.com':
            url = 'https://www.bet365.com/'

        try:
            self.driver.get(url)
            time.sleep(4)
            #bet365balance = self.driver.find_element_by_class_name('hm-MainHeaderMembersWide_Balance').text
            bet365balance = self.driver.find_element_by_class_name('hm-Balance').text
            # hm-Balance
            bet365balance = bet365balance.split(',')[0]
            bet365balance = bet365balance.strip()
            bet365balance = bet365balance.strip('£')
            bet365balance = bet365balance.replace(' ', '')
            bet365balance = float(bet365balance)
            self.current_account_balance = bet365balance
            return bet365balance
        except Exception as er:
            print(f'Не удалось получть баланс аккаунта {self.bet365_account_name} для отправки уведомлений', er)

            return 0

    def close_session(self):
        self.driver.quit()


class FireFoxForPimatch:
    def __init__(self):
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

        self.driver = driver
        self.driver.set_page_load_timeout(75)
        time.sleep(10)
        input('Смените VPN:')

        self.driver.get('https://www.parimatch.ru/')

    def get_all_coef_from_url(self, url):
        self.driver.get(url)
        time.sleep(1)
        AllCoef = self.driver.find_elements_by_class_name('_3Sa1tkZVXvesvtPRE_cUEV')
        for i in range(30):
            if len(AllCoef) == 0:
                time.sleep(0.5)
                AllCoef = self.driver.find_elements_by_class_name('_3Sa1tkZVXvesvtPRE_cUEV')
                continue
            else:
                AllCoef2 = []
                for i in range(len(AllCoef)):
                    AllCoef2.append(AllCoef[i].text)
                return  AllCoef2

        return []

    def find_coef(self, url, bet_type):
        # ожидание загрузки коэффициентов
        self.driver.get(url)
        time.sleep(1)
        AllCoef = self.driver.find_elements_by_class_name('_3Sa1tkZVXvesvtPRE_cUEV')
        not_good_flag = True
        for i in range(30):
            if len(AllCoef) == 0:
                time.sleep(0.5)
                AllCoef = self.driver.find_elements_by_class_name('_3Sa1tkZVXvesvtPRE_cUEV')
                continue
            else:
                not_good_flag = False
        if not_good_flag:
            print('Нет ставок(вообще)')
            return 'Нет ставок(вообще)'

        bets_blocks = self.driver.find_elements_by_class_name('_2NQKPrPGvuGOnShyXYTla8 ')
        if bet_type == 'WIN__P1' or bet_type == 'WIN__P2' or bet_type == 'WIN__PX':
            return self.win(bet_type)
        elif bet_type == 'WIN__12' or bet_type == 'WIN__X2' or bet_type == 'WIN__1X':
            return self.double_win(bet_type)
        elif bet_type[:13] == 'TOTALS__UNDER' or bet_type[:12] == 'TOTALS__OVER':
            return self.total_over__under(bet_type)
        # P1__TOTALS__UNDER(1.5)
        elif bet_type[:10] == 'P1__TOTALS' or bet_type[:10] == 'P2__TOTALS':
            return self.total_over__under_of_team(bet_type)
        else:
            print(bet_type)
            print('Неизвестный вид ставки')
            return 'Неизвестный вид ставки returned'

    def win(self, bet_type):
        bets_blocks = self.driver.find_elements_by_class_name('_2NQKPrPGvuGOnShyXYTla8 ')
        not_found_flag = True
        for i in range(len(bets_blocks)):
            try:
                block_ = bets_blocks[i]
                text_ = block_.find_element_by_class_name('_3vvZ3gaLgFJ2HYlmceiqzV').text
                # print(text_)
            except:
                return 'Коэффициенты изменились'
            if text_ == 'Победитель матча (основное время)':
                not_found_flag = False
                print('Ставка на париматч найдена!')
                break

        if not_found_flag:
            print('Ставка на париматч не найдена')
            return -1

        coefs = block_.find_elements_by_class_name('_3X0TBSCUiGrpBC5hAY66Pr')
        # for coef in coefs:
        #     print(coef.text)

        if bet_type == 'WIN__P1':
            return coefs[0].text
        elif bet_type == 'WIN__P2':
            return coefs[-1].text
        else:
            return coefs[1].text

    def double_win(self, bet_type):
        bets_blocks = self.driver.find_elements_by_class_name('_2NQKPrPGvuGOnShyXYTla8 ')
        not_found_flag = True
        for i in range(len(bets_blocks)):
            try:
                block_ = bets_blocks[i]
                text_ = block_.find_element_by_class_name('_3vvZ3gaLgFJ2HYlmceiqzV').text
                # print(text_)
            except:
                return 'Коэффициенты изменились'
            # print(text_)
            if text_ == 'Двойной исход':
                not_found_flag = False
                print('Ставка на париматч найдена')
                break

        if not_found_flag:
            print('Ставка не найдена')
            return -1

        coefs = block_.find_elements_by_class_name('_3X0TBSCUiGrpBC5hAY66Pr')
        # for coef in coefs:
        #     print(coef.text)

        if bet_type == 'WIN__1X':
            return coefs[0].text
        elif bet_type == 'WIN__X2':
            return coefs[-1].text
        else:
            return coefs[1].text

    def total_over__under(self, bet_type):
        bets_blocks = self.driver.find_elements_by_class_name('_2NQKPrPGvuGOnShyXYTla8 ')
        not_found_flag = True
        for i in range(len(bets_blocks)):
            try:
                block_ = bets_blocks[i]
                text_ = block_.find_element_by_class_name('_3vvZ3gaLgFJ2HYlmceiqzV').text
                # print(text_)
            except:
                return 'Коэффициенты изменились'
            # print(text_)
            if text_ == 'Тотал':
                not_found_flag = False
                print('Ставка Тотал на париматч найдена')
                break

        if not_found_flag:
            print('Ставка Тотал не найдена')
            return -1

        total_value = block_.find_element_by_class_name('_3PG_TMtKEMzUVW6dfZLkWt').text
        coefs = block_.find_elements_by_class_name('_3X0TBSCUiGrpBC5hAY66Pr')

        needed_total = bet_type.split('(')
        needed_total = needed_total[-1]
        needed_total = needed_total.strip(')')
        needed_total = needed_total.strip('')

        # print(f'Нужный тотал: {needed_total}')
        # print(f'Тотал на сайте: {total_value}')
        if needed_total == total_value:
            if 'OVER' in bet_type:
                return coefs[0].text
            else:
                return coefs[-1].text
        else:
            print(f'Размер тотала изменился с {needed_total} -> {total_value}')

    def total_over__under_of_team(self, bet_type):
        bets_blocks = self.driver.find_elements_by_class_name('_2NQKPrPGvuGOnShyXYTla8 ')
        not_found_flag = True
        total_counter = 0
        bet_block = []

        for i in range(len(bets_blocks)):
            try:
                block_ = bets_blocks[i]
                text_ = block_.find_element_by_class_name('_3vvZ3gaLgFJ2HYlmceiqzV').text
                # print(text_)
            except:
                return 'Коэффициенты изменились'
            print(text_)
            if 'Индивидуальный тотал' in text_:
                if 'P2' in bet_type:
                    if total_counter == 1:
                        not_found_flag = False
                        print('Ставка Тотал на париматч найдена')
                        break
                    else:
                        total_counter += 1
                else:
                    not_found_flag = False
                    print('Ставка Тотал на париматч найдена')
                    break


        if not_found_flag:
            print('Ставка Тотал не найдена')
            return -1

        total_value = block_.find_element_by_class_name('_3PG_TMtKEMzUVW6dfZLkWt').text
        coefs = block_.find_elements_by_class_name('_3X0TBSCUiGrpBC5hAY66Pr')

        needed_total = bet_type.split('(')
        needed_total = needed_total[-1]
        needed_total = needed_total.strip(')')
        needed_total = needed_total.strip('')

        # print(f'Нужный тотал: {needed_total}')
        # print(f'Тотал на сайте: {total_value}')
        if needed_total == total_value:
            if 'OVER' in bet_type:
                return coefs[0].text
            else:
                return coefs[-1].text
        else:
            print(f'Размер тотала изменился с {needed_total} -> {total_value}')










