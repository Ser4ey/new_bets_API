from chromdriver_class import FireFoxDriverMainNoAutoOpen, FireFoxForPimatch, GetWorkAccountsList
from google_sheets_API import AccountsBet365_from_google, GoogleAPIWorker, google_table_api
import datetime
from multiprocessing.dummy import Pool
import time
from telegram_API import telegram_notify1
import data
from API_worker import APIWorker1
from logger_file import logWorker1


def make_bet_multipotok(All_elements_array):
    print('Ставим ставку на одном из аккаунтов')
    driver, sport, url, bet_type, coef = All_elements_array
    try:
        driver.make_any_sport_bet(sport, url, bet_type, coef)
    except Exception as er:
        print(f'Ошибка при проставлении ставки: {er}')
        driver.reanimaite_bet365com()


def reanimate_bet365com(driver):
    try:
        driver.reanimaite_bet365com()
    except:
        pass


def cheeck_porezan_li_account(driver):
    try:
        driver.check_is_account_not_valid_mean_porezan()
    except Exception as er:
        print(f'Ошибка при определении порезки для - {driver.bet365_login}\nError: {er}')


def log_in_driver(driver_class):
    login = driver_class.bet365_login
    passwd = driver_class.bet365_password
    try:
        driver_class.log_in_bet365_v2(login, passwd)
    except Exception as er:
        print(f'1Ошибка при входе в аккаунт. Error:{er}')


def open_stable_bet365(driver_class):
    driver_class.restart_browser_and_bet365_account(check_valid=False)


def get_new_accounts_from_info(list_of_start_info):
    # запускаем аккаунты
    List_of_bet_account = []
    countries = []
    Set_of_countries = set()

    for i in list_of_start_info:
        countries.append(i[3])

    for i in countries:
        Set_of_countries.add(i)

    Dict_of_Drivers_count = {}

    for i in Set_of_countries:
        Dict_of_Drivers_count[i] = countries.count(i)

    start_time_for_all = time.time()
    for i in Set_of_countries:
        print(f'Открываем {Dict_of_Drivers_count[i]} аккаунта для {i}')
        start_time_for_type = time.time()
        accounts_get_class = GetWorkAccountsList(number_of_accounts=Dict_of_Drivers_count[i], vpn_country=i)
        Accounts = accounts_get_class.return_Browser_List()

        for account_info in list_of_start_info:
            bet365login, bet365password, bet_value, vpn_country = account_info
            if vpn_country != i:
                continue

            driver_class = FireFoxDriverMainNoAutoOpen(
                driver=Accounts.pop(-1),
                login=bet365login,
                password=bet365password,
                bet_value=bet_value,
                vpn_country=vpn_country
            )

            List_of_bet_account.append(driver_class)
        print(f'{Dict_of_Drivers_count[i]} аккаунтов для {i} открыты за {time.time() - start_time_for_type}')

    print(f'Все аккаунты успешно открыты за {time.time() - start_time_for_all}')
    # авторизация аккаунтов
    with Pool(processes=len(List_of_bet_account)) as p:
        p.map(log_in_driver, List_of_bet_account)

    print(f'Все аккаунты успешно авторизованы!')

    # предварительный поиск порезанных аккаунтов
    with Pool(processes=len(List_of_bet_account)) as p:
        p.map(cheeck_porezan_li_account, List_of_bet_account)

    return List_of_bet_account


def check_is_account_froze(driver):
    pass
    # result = driver.restart_browser_and_bet365_account()
    # # Аккаунт завис
    # if result:
    #     Account_start_date = [[
    #         driver.bet365_login,
    #         driver.bet365_password,
    #         driver.bet_value,
    #         driver.vpn_country
    #     ]]
    #
    #     new_driver = get_new_accounts_from_info(Account_start_date)
    #     driver.driver = new_driver[0].driver


class GetNewAccountsListHigh:
    def __init__(self, reboot_time=60*60):
        self.time_point = time.time()
        self.reboot_time = reboot_time

    def get_new_accounts_list(self):
        '''Возвращает список новых аккаунтов'''
        list_of_start_info = []
        AccountsBet365_from_google = google_table_api.get_all_accounts_date()
        i1 = 1

        for i in range(len(AccountsBet365_from_google)):
            account_data = AccountsBet365_from_google[i]
            if account_data[5] == 'Да':
                print(f'Аккаунт {account_data[0]} - порезан. Не окрываем его.')
                continue
            start_info = [account_data[0], account_data[1], account_data[2], account_data[3]]
            list_of_start_info.append(start_info)
            i1 += 1

        List_of_bet_account = get_new_accounts_from_info(list_of_start_info)
        GoogleAPIWorker.rewrate_google_sheet()

        return List_of_bet_account

    def restart_all_accounts_and_return_new_by_time_check(self, accounts_list_to_close=[]):
        '''Принемает список старых аккаунтов, закрывает их, если прошло более x ремени
        и возвращаем массив с новыми(или старыми) аккаунтами'''
        time_now = time.time()

        time_delta = time_now - self.time_point
        if time_delta < self.reboot_time:
            print(f'С момента перезагрузки прошло {time_delta} сек. Не перезапускаем аккаунты(интервал: {self.reboot_time})')
            return accounts_list_to_close

        print(f'С момента перезагрузки прошло {time_delta} сек. Перезапуск!')
        for i in range(len(accounts_list_to_close)):
            try:
                driver_class_ = accounts_list_to_close[i]
                driver_class_.driver.close()
                driver_class_.driver.quit()
                print(f'Аккаунт {i+1}/{len(accounts_list_to_close)} закрыт')
            except:
                print(f'Аккаунт {i+1}/{len(accounts_list_to_close)} не удалось закрыть!')

        self.time_point = time.time()
        print(f'Обновляем время, новая точка: {self.time_point}')

        return self.get_new_accounts_list()


NewAccountsGetterHigh = GetNewAccountsListHigh()

driverParimatch = FireFoxForPimatch(data.VPN_dict['RU'])

List_of_bet_account = NewAccountsGetterHigh.get_new_accounts_list()

AllBetsSet = set()
reboot_counter = 0
porezan_counter = 0
graphic_bet_telegram_counter = 0
error_flag = False

while True:
    # перезапуск аккаунтов каждый час
    List_of_bet_account = NewAccountsGetterHigh.restart_all_accounts_and_return_new_by_time_check(List_of_bet_account)

    # add new accounts from google sheets
    new_accounts_info = GoogleAPIWorker.return_new_accounts_info()
    # список новых аккаунтов
    list_of_new_info = []
    for i in range(len(new_accounts_info)):
        account_data = new_accounts_info[i]
        new_info = [account_data[0], account_data[1], account_data[2], account_data[3]]
        list_of_new_info.append(new_info)

    # print('list of new info:', list_of_new_info)

    if len(list_of_new_info) > 0:
        print('Запускаем новые аккаунты')
        List_of_bet_account += get_new_accounts_from_info(list_of_new_info)
    else:
        print('Нет новых аккаунтов')

    # Вывод текущего времени
    now = datetime.datetime.now()
    now = now.strftime('%H:%M:%S')
    print(now)

    # реанимация .com аккаунтов
    with Pool(processes=len(List_of_bet_account)) as p:
        A = [i for i in List_of_bet_account]
        p.map(reanimate_bet365com, A)

    if porezan_counter % 6 == 0:
        # i_porez = 0
        try:
            with Pool(processes=len(List_of_bet_account)) as p:
                p.map(cheeck_porezan_li_account, List_of_bet_account)
        except Exception as er:
            print(er)

        # while i_porez < len(List_of_bet_account):
        #     if not List_of_bet_account[i_porez].is_valud_account:
        #         if GoogleAPIWorker.Accounts[i_porez][5] == 'Да':
        #             i_porez += 1
        #             continue
        #         GoogleAPIWorker.Accounts[i_porez][5] = 'Да'
        #         telegram_text = f'{List_of_bet_account[i_porez].bet365_login} - порезан. Баланс: {List_of_bet_account[i_porez].get_balance()} '
        #         telegram_notify1.telegram_bot_send_message(telegram_text)
        #         print(f'Аккаунт {List_of_bet_account[i_porez].bet365_login} - порезан')
        #         List_of_bet_account[i_porez].driver.quit()
        #         List_of_bet_account.pop(i_porez)
        #     else:
        #         i_porez += 1

        # определение порезки аккаунтов алгоритм 2.0
        for i in range(len(List_of_bet_account)):
            if not List_of_bet_account[i].is_valud_account:

                account_google_line = 'no'
                # сопоставление аккаунта в гугл таблицах аккаунту в массиве
                for g in range(len(GoogleAPIWorker.Accounts)):
                    google_name = GoogleAPIWorker.Accounts[g][0]
                    if google_name == List_of_bet_account[i].bet365_login:
                        account_google_line = g
                        print(f'{google_name} = {List_of_bet_account[i].bet365_login}, g:{g} = A{i}')
                        break

                if account_google_line == 'no':
                    print('Не удалось найти аккаунт в гугл таблице!')


                if GoogleAPIWorker.Accounts[account_google_line][5] == 'Да':
                    print('Аккаунт уже определён как порезанный (?)')
                    continue

                GoogleAPIWorker.Accounts[account_google_line][5] = 'Да'
                print(f'Аккаунт {List_of_bet_account[i].bet365_login} - порезан ({GoogleAPIWorker.Accounts[account_google_line][0]})')
                telegram_text = f'{List_of_bet_account[i].bet365_login} - порезан. Баланс: {List_of_bet_account[i].get_balance()} '
                telegram_notify1.telegram_bot_send_message(telegram_text)
                print(f'Аккаунт {List_of_bet_account[i].bet365_login} - порезан')
                List_of_bet_account[i].driver.quit()
                # List_of_bet_account.pop(i)


    GoogleAPIWorker.rewrate_google_sheet()
    porezan_counter += 1
    print(f'Осталось рабочих аккаунтов: {len(List_of_bet_account)}')

    # цикл проставления ставок
    for j1 in range(80):
        time.sleep(7)

        try:
            fork_info = APIWorker1.send_request_to_API(old_bets_set=AllBetsSet)
            if not fork_info:
                continue
            print(fork_info)
        except Exception as er:
            print('Ошибка при отправке API запроса:', er)
            time.sleep(10)
            continue

        if fork_info['fork_id'] in AllBetsSet:
            print(f"Ставка {fork_info['fork_id']} уже проставлена! (main process)")
            time.sleep(10)
            continue
        AllBetsSet.add(fork_info['fork_id'])

        try:
            second_coef = driverParimatch.find_coef_for_any_sport(fork_info['sport_name'], fork_info['parimatch_href'], fork_info['parimatch_type'])
            print(f'Коэффициент на париматч: {second_coef}')
            try:
                float(second_coef)
            except:
                print('Ставка не поддерживается')
                continue
            if float(second_coef) + 0.05 < float(fork_info['parimatch_coef']):
                print('Коэффициет на париматч упал!', f'{fork_info["parimatch_coef"]} -> {second_coef}')
                continue
        except:
            print('Не удалось получить коэффициент для париматч')
            continue

        # добавление ставки в логи
        print('Добавляем ставку в лог файл')
        logWorker1.write_row_in_log_file(
        [
            fork_info['BK1_name'],
            fork_info['BK2_name'],
            fork_info['BK1_coef'],
            fork_info['BK2_coef'],
            fork_info['BK1_game_name'],
            fork_info['count_of_BK1_plus_forks'],
            fork_info['count_of_BK2_plus_forks'],

        ]
        )
        # проставление ставок на всех аккаунтах (Pool)
        try:
            print('-'*100)
            A = []
            for i in range(len(List_of_bet_account)):
                account_arr = [List_of_bet_account[i],
                               fork_info['sport_name'],
                                fork_info['bet365_href'],
                                fork_info['bet365_type'],
                                fork_info['bet365_coef']]
                A.append(account_arr)

            with Pool(processes=len(List_of_bet_account)) as p:
                p.map(make_bet_multipotok, A)
        except:
            print('Ошибка при проставлении ставок (Pool)')

        time.sleep(30)

    AllBetsSet = set()







