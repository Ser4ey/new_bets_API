import time


class LogWorker:
    def __init__(self, path_to_log_file):
        self.path_to_log_file = path_to_log_file
        self.log_info = []

    def write_row_in_log_file(self, row):
        '''row - интерируемый'''
        with open(self.path_to_log_file, 'a', encoding='utf-8') as file:
            str_row = [str(i) for i in row]

            row_line = ','.join(str_row) + '\n'
            file.write(row_line)

        print(f'Строка записана: {row_line}')

    def get_all_log_data(self):
        with open(self.path_to_log_file, 'r', encoding='utf-8') as file:
            log_info = file.readlines()
            log_info = [i.strip() for i in log_info if i != '']
        print(log_info)
        return log_info

    def get_info_from_log_string(self):
        return ''






logWorker1 = LogWorker('logFile.txt')

# logWorker1.write_row_in_log_file([1,2,3,'dd'])
logWorker1.get_all_log_data()


