

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
    # START OF PROGRAM

    porezan_counter = 1
    # предварительный поиск порезанных аккаунтов
    with Pool(processes=len(List_of_bet_account)) as p:
        p.map(cheeck_porezan_li_account, List_of_bet_account)
    i_porez = 0
    while i_porez < len(List_of_bet_account):
        if not List_of_bet_account[i_porez].is_valud_account:
            telegram_text = f'{List_of_bet_account[i_porez].bet365_login} - порезан. Баланс: {List_of_bet_account[i_porez].get_balance()} '
            telegram_notify1.telegram_bot_send_message(telegram_text)
            delete_account_from_txt_by_login(List_of_bet_account[i_porez].bet365_login)
            print(f'Аккаунт {List_of_bet_account[i_porez].bet365_login} - порезан')
            List_of_bet_account[i_porez].driver.quit()
            List_of_bet_account.pop(i_porez)
        else:
            i_porez += 1

    print(f'Осталось рабочих аккаунтов: {len(List_of_bet_account)}')
    # завершение поиска порезанных аккаунтов
