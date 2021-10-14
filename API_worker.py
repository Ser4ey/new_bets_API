import requests
import json
import time


TOKEN = 'ec02c59dee6faaca3189bace969c22d7'
URL = 'http://212.109.216.193:8111/forks'

params = {
    "token": TOKEN,
    "bk2_name": "bet365,parimatch_ru_new",
    "sport": "soccer",
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
            print('Нет вилок')
            return False

        bet1 = 'No'
        for i in respons:
            if i['is_cyber'] == '1':
                bet1 = i
                break
        if bet1 == 'No':
            print('Нет вилок на кибер футбол')
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

        return {
            'bet365_href': bet365_href,
            'bet365_type': bet365_type,
            'bet365_coef': bet365_coef,
            'parimatch_href': parimatch_href,
            'parimatch_type': parimatch_type,
            'parimatch_coef': parimatch_coef,
            'bet_all_data': bet1,
            'responce': respons
        }


APIWorker1 = APIWork(TOKEN, URL, params)

for i in range(100):
    r = APIWorker1.send_request_to_API()
    print(r)
    time.sleep(5)



