from data import sheet_id
import httplib2
# import apiclient.discovery
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials
import data
import time


class GoogleAPI:
    def __init__(self, sheet_id):
        # создаём сейссию с таблицей
        CREDENTIALS_FILE = 'creds.json'
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        httpAuth = credentials.authorize(httplib2.Http())
        self.service = discovery.build('sheets', 'v4', http=httpAuth)

        self.spreadsheet_id = sheet_id
        self.write_row(current_line=1,
                       row=['Login', 'Password', 'Bet value(%5)', 'VPN',
                            'Статус работы(in_work, need_start, dead)', 'Порезан'])

    def write_row(self, row, current_line=2):
        values = self.service.spreadsheets().values().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={
                "valueInputOption": "USER_ENTERED",
                "data": [
                    {f"range": f"A{current_line}:F{current_line}",
                     "majorDimension": "ROWS",
                     "values": [row]},

                ]
            }
        ).execute()

    def write_many_rows(self, many_rows_list, start_line=2):
        for i in range(len(many_rows_list)):
            row = many_rows_list[i]
            self.write_row(row, start_line)
            start_line += 1

    def get_all_accounts_date(self):
        # возвращает данные аккаунтов, исключая 1 строку заголовков
        ranges = ["A1:G1000"]
        results = self.service.spreadsheets().values().batchGet(spreadsheetId=self.spreadsheet_id,
                                                           ranges=ranges,
                                                           valueRenderOption='FORMATTED_VALUE',
                                                           dateTimeRenderOption='FORMATTED_STRING').execute()
        sheet_user_values = results['valueRanges'][0]['values']

        sheet_user_values = sheet_user_values[1:]
        clean_accounts = []

        for account_ in sheet_user_values:
            if account_info[0].strip() != '':
                clean_accounts.append(account_)

        return clean_accounts


class WorkWithGoogleAPI:
    def __init__(self, google_api_exemple: GoogleAPI):
        self.google_api = google_api_exemple
        self.Accounts = self.google_api.get_all_accounts_date()

        for account in self.Accounts:
            if account[5].strip() == '':
                account[5] = 'Нет'

    def rewrate_google_sheet(self):
        for i in range(len(self.Accounts)):
            account = self.Accounts[i]
            if account[5] == 'Да':
                account[4] = 'Dead'
            else:
                account[4] = 'In work'

        self.google_api.write_many_rows(self.Accounts)

    def return_new_accounts_info(self):
        # возвращает данные для регистрации новых аккаунтов
        new_accounts = self.google_api.get_all_accounts_date()

        return_accounts = new_accounts[len(self.Accounts):]

        self.Accounts = new_accounts
        for account in self.Accounts:
            if account[5].strip() == '':
                account[5] = 'Нет'

        return return_accounts


google_table_api = GoogleAPI(sheet_id)

# A = [[f'testname{i+1}', f'testpass{i+1}', '%5', 'UK', 'in_work', 'Нет'] for i in range(10)]
# # print(A)
# google_table_api.write_many_rows(A)
# google_table_api.get_all_accounts_date()

AccountsBet365_from_google = []
accounts_ = google_table_api.get_all_accounts_date()

for i in range(len(accounts_)):
    account_info = accounts_[i]

    if account_info[0].strip() == '':
        break

    data_ = account_info[:]
    AccountsBet365_from_google.append(
        {'bet365_login': data_[0], 'bet365_password': data_[1], 'bet_value': data_[2], 'vpn_country': data_[3]},
    )

print(AccountsBet365_from_google)


GoogleAPIWorker = WorkWithGoogleAPI(google_api_exemple=google_table_api)