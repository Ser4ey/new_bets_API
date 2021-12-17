import requests
import json
import time
from datetime import datetime
import data

# def check_time(time_string):
#     # BK1_score	"1:1 65:14"
#     # print(time_string)
#     game_time = time_string.split(' ')[-1]
#     game_minutes = game_time.split(':')[0]
#
#     if int(game_minutes) >= 8:
#         return False
#     return True

TOKEN = 'ec02c59dee6faaca3189bace969c22d7'
URL = 'http://api.oddscp.com:8111/valuebets'

min_fi_valuebet = data.min_fi_valuebet

params = {
    "token": TOKEN,
    "sport": "soccer",
    "bk_name": "bet365",
    # 'get_cfs': '1',
    'min_fi': min_fi_valuebet,

}

# https://github.com/Ser4ey/new_bets_API.git
class APIWork:
    def __init__(self, TOKEN: str, URL: str, params: dict):
        self.TOKEN = TOKEN
        self.URL = URL
        self.params = params
        self.forks_ids = set()

    def send_request_to_API(self, old_bets_set=set()):
        # список уже проставленных ставок

        try:
            r = requests.get(self.URL, params=self.params)
            # print(r.url)
            respons = json.loads(r.text)
        except Exception as er:
            print('!'*100)
            print('Ошибка при отправке запроса к API')
            print(er)
            try:
                print(r.status_code)
            except:
                print('Status code: None')
            print('!'*100)
            time.sleep(20)
            return False

        if len(respons) < 1:
            print('Нет вилок', datetime.now())
            return False

        bet1 = 'No'
        for i in respons:
            if not (i['fork_id'] in old_bets_set):
                old_bets_set.add(i['fork_id'])
                bet365_line = '1'
                other_line = '2'

                # проверка на кибер спорт (убрана)
                # if i['BK1_league'] == "Esoccer Battle - 8 mins play":
                #     print('------Вилка найдена------')
                #     print('Ставка на киберфутбол')
                # else:
                #     print('Ставка не на киберфутбол')
                #     continue

                if float(i[f'BK{bet365_line}_cf']) >= 2:
                    print(f'Коэффициент на bet365:', i[f'BK{bet365_line}_cf'])
                    bet1 = i
                    break
                else:
                    print('Коэффициент на bet365 < 2', i[f'BK{bet365_line}_cf'])


        if bet1 == 'No':
            print('Нет вилок на кибер футбол', datetime.now())
            return False

        fork_id = bet1['fork_id']
        sport_name = bet1['sport']

        bet365_href = bet1[f'BK{bet365_line}_href']

        bet365_type = bet1[f'BK{bet365_line}_bet']

        bet365_coef = bet1[f'BK{bet365_line}_cf']
        other_coef = bet1[f'BK{other_line}_cf']

        return {
            'sport_name': sport_name,
            'bet365_href': bet365_href,
            'bet365_type': bet365_type,
            'bet365_coef': bet365_coef,
            'other_coef': other_coef,
            'fork_id': fork_id,
            'bet_all_data': bet1,
            'responce': respons,
        }


APIWorker1 = APIWork(TOKEN, URL, params)

AllForks = set()


