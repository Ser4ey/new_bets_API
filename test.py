import json


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
# print(cfs1)
cfs1 = {'MTU': '1.58', 'OLC': '1.61', 'BT3': '1.727', 'BNB': '1.62', 'VBT': '1.55', 'OLP': '1.61', 'BOR': '1.55', 'STX': '1.6', 'LEO': '1.61', 'MTH': '1.58', 'MTB': '1.58', 'PAC': '1.5', 'PAN': '1.5', 'LBT': '1.47', 'WLN': '1.43'}


print(cfs1)
print(find_max_in_dict(cfs1))
print(find_min_in_dict(cfs1))








