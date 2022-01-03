import time


class RestartAccountsClass:
    def __init__(self):
        self.time_point = time.time()
        '''Принемает список старых аккаунтов, закрывает их'''
    def restart_all_accounts_and_return_new(self, accounts_list=[]):
        time_now = time.time()

        time_delta = time_now - self.time_point
        print(time_delta, time_delta > 1)


restartClass1 = RestartAccountsClass()

while True:
    input(':::')
    restartClass1.restart_all_accounts_and_return_new()