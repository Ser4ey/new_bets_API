from chromdriver_class import FireFoxDriverMain, FireFoxForPimatch
from data import AccountsBet365
import datetime
from multiprocessing.dummy import Pool
import time
from API_worker import APIWorker1


def make_bet_multipotok(All_elements_array):
    print('Ставим ставку на одном из аккаунтов')
    driver, url, bet_type, coef = All_elements_array
    try:
        driver.make_cyber_football_bet(url, bet_type, coef)
    except:
        print('Реанимация аккаунта')
        driver.reanimaite_bet365com()

def reanimate_bet365com(driver):
    driver.reanimaite_bet365com()


driverParimatch = FireFoxForPimatch()

List_of_bet_account = [0] * len(AccountsBet365)
i1 = 1
for i in range(len(AccountsBet365)):
    print(f'Запуск аккаунта {i1}')
    account_data = AccountsBet365[i]
    # запускаем аккаунт пока он не запустится
    while True:
        try:
            driver2 = FireFoxDriverMain(account_data['bet_value'])
            driver2.log_in_bet365(login=account_data['bet365_login'], password=account_data['bet365_password'])
            List_of_bet_account[i] = driver2
            break
        except:
            print('Ошибка при запуске аккаунта')
            print(f'Повторный запуск аккаунта {i1}')
            try:
                driver2.driver.close()
                driver2.driver.quit()
            except:
                pass

    i1 += 1
AllBetsSet = set()

reboot_counter = 0
graphic_bet_telegram_counter = 0
error_flag = False

while True:
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
            print(f"Ставка {fork_info['fork_id']} уже проставлена!")
            time.sleep(10)
            continue
        AllBetsSet.add(fork_info['fork_id'])


        second_coef = driverParimatch.find_coef(fork_info['parimatch_href'], fork_info['parimatch_type'])
        print(f'Коэффициент на париматч: {second_coef}')
        try:
            float(second_coef)
        except:
            print('Ставка не поддерживается')
            continue
        if float(second_coef) < float(fork_info['parimatch_coef']):
            print('Коэффициет на париматч упал!', f'{fork_info["parimatch_coef"]} -> {second_coef}')
            continue

        # проставление ставок на всех аккаунтах (Pool)
        try:
            print('-'*100)
            A = []
            for i in range(len(AccountsBet365)):
                account_arr = [List_of_bet_account[i],
                                fork_info['bet365_href'],
                                fork_info['bet365_type'],
                                fork_info['bet365_coef']]
                A.append(account_arr)

            with Pool(processes=len(AccountsBet365)) as p:
                p.map(make_bet_multipotok, A)
        except:
            print('Ошибка при проставлении ставок (Pool)')

        time.sleep(30)

    AllBetsSet = set()

    # Вывод текущего времени
    now = datetime.datetime.now()
    now = now.strftime('%H:%M:%S')
    print(now)

    # реанимация .com аккаунтов
    with Pool(processes=len(AccountsBet365)) as p:
        A = [i for i in List_of_bet_account]
        p.map(reanimate_bet365com, A)


