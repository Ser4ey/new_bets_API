def delete_account_from_txt_by_login(login: str):
    with open('accounts_list.txt', 'r', encoding='utf-8') as file:
        lines_with_accounts = file.readlines()

    with open('accounts_list.txt', 'w', encoding='utf-8') as file:
        for line in lines_with_accounts:
            if not login in line:
                file.write(line)
            else:
                print(f'{login} - удалён из аккаунтов!')



delete_account_from_txt_by_login('Eliza1971')