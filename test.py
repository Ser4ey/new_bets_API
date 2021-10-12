try:
    a = 1
    no_valid_flag = False

    try:
        a = 1
        no_valid_flag = True
    except:
        pass
    try:
        driver1.driver.find_element_by_class_name('withdrawal-restriction')
        print('порезан2')
        no_valid_flag = True
    except:
        pass

    if no_valid_flag:
        raise Exception('Не рабочий аккунт')
    print('Рабочий аккаунт')
    is_good = True
except:
    print('Порезан')

