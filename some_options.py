import requests
import json
import time
from datetime import datetime
from data import min_fi


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
    "bk2_name": "bet365,parimatch_ru_new",
    "sport": "basketball",
    'get_cfs': '1',
    'min_fi': min_fi,
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
                print('Status code:', r.status_code)
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
            if (i['sport'] == 'basketball') or (i['is_cyber'] == '1'):
                if not (i['fork_id'] in old_bets_set):
                    bet365_line = '2'
                    parimatch_line = '1'
                    if i['BK1_name'] == 'bet365':
                        bet365_line = '1'
                        parimatch_line = '2'

                    if float(i[f'BK{bet365_line}_cf']) >= 2:
                        bet1 = i
                        break
                    else:
                        print('Коэффициент на bet365 < 2', i[f'BK{bet365_line}_cf'])


        if bet1 == 'No':
            print('Нет вилок на кибер футбол|баскетбол', datetime.now())
            return False

        bet365_line = '2'
        parimatch_line = '1'
        if bet1['BK1_name'] == 'bet365':
            bet365_line = '1'
            parimatch_line = '2'

        sport_name = bet1['sport']

        bet365_href = bet1[f'BK{bet365_line}_href']
        parimatch_href = bet1[f'BK{parimatch_line}_href']

        bet365_type = bet1[f'BK{bet365_line}_bet']
        parimatch_type = bet1[f'BK{parimatch_line}_bet']

        bet365_coef = bet1[f'BK{bet365_line}_cf']
        parimatch_coef = bet1[f'BK{parimatch_line}_cf']

        if float(bet365_coef) < 2:
            print('Коэффициент на бет365 < 2')
        # список коэффициентов по всем бк
        cfs1 = bet1['cfs1']
        cfs1 = json.loads(cfs1)

        cfs2 = bet1['cfs2']
        cfs2 = json.loads(cfs2)

        list_of_cfs = [0, cfs1, cfs2]
        fork_id = bet1['fork_id']

        count_of_bet365_plus_forks = find_number_of_plus_bets(
            our_coef=bet365_coef,
            bk_name='BT3',
            opposite_forks=list_of_cfs[int(parimatch_line)]
        )

        count_of_parimatch_plus_forks = find_number_of_plus_bets(
            our_coef=parimatch_coef,
            bk_name='PAN',
            opposite_forks=list_of_cfs[int(bet365_line)]
        )

        print('Выигрышных ставок с bet365:', count_of_bet365_plus_forks)
        print('Выигрышных ставок с parimatch:', count_of_parimatch_plus_forks)
        if count_of_parimatch_plus_forks >= count_of_bet365_plus_forks:
            print('Bet365 не инициатор')
            return False

        return {
            'sport_name': sport_name,
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

AllForks = set()

for i in range(1000):
    time.sleep(5)
    r = APIWorker1.send_request_to_API(old_bets_set=AllForks)
    if not r:
        continue

    AllForks.add(r['fork_id'])
    print(r)

#






