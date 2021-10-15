def find_initiator(our_coef: str, bk_name: str, opposite_forks: dict):
    plus_forks_number = 0

    opposite_forks.pop(bk_name)
    for bk, coef in opposite_forks.items():
        profit = 1 - (1/float(our_coef) + 1/float(coef))
        if profit > 0:
            plus_forks_number += 1

    print(plus_forks_number)
    return plus_forks_number


cfs1 = {'MTU': '1.58', 'OLC': '1.61', 'BT3': '1.727', 'BNB': '1.62', 'VBT': '1.55', 'OLP': '1.61', 'BOR': '1.55', 'STX': '1.6', 'LEO': '1.61', 'MTH': '1.58', 'MTB': '1.58', 'PAC': '1.5', 'PAN': '1.5', 'LBT': '1.47', 'WLN': '1.43'}


find_initiator('2.8', 'BT3', cfs1)






