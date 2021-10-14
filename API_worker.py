import requests
import json
import time
from datetime import datetime


def find_max_in_dict(d: dict):
    max_coef = 0
    best_bk = 'None'

    for name, coef in d.items():
        if float(coef) > max_coef or (name == 'BT3' and float(coef) >= max_coef):
            best_bk = name
            max_coef = float(coef)

    return best_bk


def find_min_in_dict(d: dict):
    min_coef = 100000
    min_bk = 'None'

    for name, coef in d.items():
        if float(coef) < min_coef:
            min_bk = name
            min_coef = float(coef)

    return min_bk


TOKEN = 'ec02c59dee6faaca3189bace969c22d7'
URL = 'http://212.109.216.193:8111/forks'

params = {
    "token": TOKEN,
    "bk2_name": "bet365,parimatch_ru_new",
    "sport": "soccer",
    'get_cfs': '1',
}


class APIWork:
    def __init__(self, TOKEN: str, URL: str, params: dict):
        self.TOKEN = TOKEN
        self.URL = URL
        self.params = params
        self.forks_ids = set()

    def send_request_to_API(self):
        r = requests.get(self.URL, params=self.params)
        respons = json.loads(r.text)

        if len(respons) < 1:
            print('Нет вилок', datetime.now())
            return False

        bet1 = 'No'
        for i in respons:
            if i['is_cyber'] == '1':
                bet1 = i
                break
        if bet1 == 'No':
            print('Нет вилок на кибер футбол', datetime.now())
            return False

        bet365_line = '2'
        parimatch_line = '1'
        if bet1['BK1_name'] == 'bet365':
            bet365_line = '1'
            parimatch_line = '2'

        bet365_href = bet1[f'BK{bet365_line}_href']
        parimatch_href = bet1[f'BK{parimatch_line}_href']

        bet365_type = bet1[f'BK{bet365_line}_bet']
        parimatch_type = bet1[f'BK{parimatch_line}_bet']

        bet365_coef = bet1[f'BK{bet365_line}_cf']
        parimatch_coef = bet1[f'BK{parimatch_line}_cf']

        # список коэффициентов по всем бк
        cfs1 = bet1['cfs1']
        cfs1 = json.loads(cfs1)

        cfs2 = bet1['cfs2']
        cfs2 = json.loads(cfs2)

        fork_id = bet1['fork_id']

        if find_max_in_dict(cfs1) == 'BT3' and find_min_in_dict(cfs2) != 'PAN':
            print('BET365 - инциатор')
        elif find_max_in_dict(cfs2) == 'BT3' and find_min_in_dict(cfs1) != 'PAN':
                print('BET365 - инциатор2')
        else:
            print('BET365 - не инициатор')
            print(cfs1)
            print(cfs2)
            return False

        return {
            'bet365_href': bet365_href,
            'bet365_type': bet365_type,
            'bet365_coef': bet365_coef,
            'parimatch_href': parimatch_href,
            'parimatch_type': parimatch_type,
            'parimatch_coef': parimatch_coef,
            'cfs1': cfs1,
            'cfs2': cfs2,
            'fork_id': fork_id,
            'bet_all_data': bet1,
            'responce': respons,
        }


APIWorker1 = APIWork(TOKEN, URL, params)

# for i in range(100):
#     time.sleep(5)
#     r = APIWorker1.send_request_to_API()
#     if not r:
#         continue
#     print(r)
#     print(r['cfs1'])
#     print(r['cfs2'])
#



