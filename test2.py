# путь к geckodriver
path_to_geckodriver = r'C:\Users\Administrator\PycharmProjects\new_bets_API\geckodriver.exe'
firefox_binary = r'C:\Program Files\Mozilla Firefox\firefox.exe'

firefox_profile_path = r'C:\Users\Administrator\AppData\Roaming\Mozilla\Firefox\Profiles\7z70kthi.default-release'

path_to_accounts_file = r'C:\Users\Administrator\Desktop\accounts_list.txt'
# получение аккаунтов
AccountsBet365 = []
with open(path_to_accounts_file, 'r', encoding='utf-8') as file:
    accounts_ = file.readlines()
    accounts_.pop(0)
    for i in range(len(accounts_)):
        if len(accounts_[i].strip()) != 0:
            data_ = accounts_[i].strip().split(';')
            AccountsBet365.append(
                {'bet365_login': data_[0], 'bet365_password': data_[1], 'bet_value': data_[2]},
            )
print(AccountsBet365)


# минимальный процент вилки
min_fi = '0'

# Данные для телеграм уведомлений
BOT_TOKEN = '1836794832:AAEZxkO6THf-TQ_xKYpbtqF5T5LNWwPSwfw'
BOT_TOKEN_GRAF = '1673449920:AAEmKCmlSxzD2IxVKKKznmsawJUzYaZsKzI'

my_id = '409524113'
pavel_id = '366274603'

Telegram_admins = [my_id, pavel_id]