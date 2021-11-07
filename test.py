import requests
import json
import time
from datetime import datetime
# from data import min_fi, min_value_of_alive_sec, max_value_of_alive_sec


def find_number_of_plus_bets(our_coef: str, bk_name: str, opposite_forks: dict):
    plus_forks_number = 0
    try:
        opposite_forks.pop(bk_name)
    except:
        pass
    for bk, coef in opposite_forks.items():
        profit = 1 - (1/float(our_coef) + 1/float(coef))
        if profit > 0:
            plus_forks_number += 1

    return plus_forks_number

TOKEN = 'ec02c59dee6faaca3189bace969c22d7'
URL = 'http://212.109.216.193:8111/forks'

params = {
    "token": TOKEN,
    "bk2_name": "bet365,fonbet",
    # "sport": "soccer",
    'get_cfs': '1',
    'min_fi': 10,
}


class APIWork:
    def __init__(self, TOKEN: str, URL: str, params: dict):
        self.TOKEN = TOKEN
        self.URL = URL
        self.params = params
        self.forks_ids = set()

    def send_request_to_API(self, old_bets_set='1'):
        # список уже проставленных ставок
        if old_bets_set == '1':
            old_bets_set = []

        try:
            r = requests.get(self.URL, params=self.params)
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
            # print('Нет вилок', datetime.now())
            return False

        for i in respons:
            bet1 = i
            sport_name = bet1['sport']
            bet_type = bet1['bet_type']
            income = bet1['income']

            bet365_line = '2'
            fonbet_line = '1'
            if bet1['BK1_name'] == 'bet365':
                bet365_line = '1'
                fonbet_line = '2'

            bet365_bet = bet1[f'BK{bet365_line}_bet']
            fonbet_bet = bet1[f'BK{fonbet_line}_bet']

            text = f'Спорт: {sport_name}; Ставка: {bet_type}; Процент: {income}; bet365: {bet365_bet}; fonbet: {fonbet_bet}\n'
            print(text)

            with open('bet_log.txt', 'a', encoding='utf-8') as file:
                file.write(text)


APIWorker1 = APIWork(TOKEN, URL, params)

AllForks = set()

for i in range(10000):
    time.sleep(5)
    APIWorker1.send_request_to_API(old_bets_set=AllForks)





