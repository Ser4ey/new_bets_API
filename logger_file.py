import time


class LogWorker:
    def __init__(self, path_to_log_file):
        self.path_to_log_file = path_to_log_file
        self.log_info = []

    def write_row_in_log_file(self, row):
        '''row - интерируемый
        [BK1_name, BK2_name, BK1_coef, BK2_coef, BK1_game_name, count_of_BK1_plus_forks, count_of_BK2_plus_forks]
        '''
        with open(self.path_to_log_file, 'a', encoding='utf-8') as file:
            str_row = [str(i) for i in row]

            row_line = '$'.join(str_row) + '\n'
            file.write(row_line)

        print(f'Строка записана: {row_line}')

    def get_all_log_data(self):
        with open(self.path_to_log_file, 'r', encoding='utf-8') as file:
            log_info = file.readlines()
            log_info = [i.strip() for i in log_info if i != '']
        print(log_info)
        return log_info

    def get_info_from_log_string(self, log_string: str):
        # [BK1_name, BK2_name, BK1_coef, BK2_coef, BK1_game_name, count_of_BK1_plus_forks, count_of_BK2_plus_forks]

        log_list = log_string.split('$')
        if len(log_list) < 7:
            print(f'Ошибка в строке лог файла: {log_string}')
            log_list = [0] * 10

        log_dict = {
            'BK1_name': log_list[0],
            'BK2_name': log_list[1],
            'BK1_coef': log_list[2],
            'BK2_coef': log_list[3],
            'BK1_game_name': log_list[4],
            'count_of_BK1_plus_forks': log_list[5],
            'count_of_BK2_plus_forks': log_list[6]

        }

        return log_dict


logWorker1 = LogWorker('logFile.txt')

# logWorker1.write_row_in_log_file([1,2,3,'dd'])
# logWorker1.get_all_log_data()


