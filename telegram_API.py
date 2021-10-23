import data
import requests

BOT_TOKEN = data.BOT_TOKEN
ADMINS = data.Telegram_admins


class TelegramNotify:
    def __init__(self, admins, bot_token):
        self.admins = admins
        self.bot_token = bot_token

    def telegram_bot_send_message(self, text):
        for admin in self.admins:
            url = f'https://api.telegram.org/bot{self.bot_token}/sendMessage?chat_id={admin}&text={text}'
            response = requests.get(url)
            # print('Telegram response:', response)

    def telegram_bot_send_photo(self, chat_id, path_to_photo):
        url = f"https://api.telegram.org/bot{self.bot_token}/sendPhoto"
        files = {'photo': open(path_to_photo, 'rb')}
        data = {'chat_id': chat_id}
        r = requests.post(url, files=files, data=data)
        return r.json()


telegram_notify1 = TelegramNotify(ADMINS, BOT_TOKEN)

# telegram_notify1.telegram_bot_send_message('Work!')
