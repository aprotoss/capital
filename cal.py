# -*- coding: utf-8 -*-



def ma(data):
    avg  = 0
    for i in data:
        avg = avg + i
    
    avg = avg / len(data)
    return avg


import pandas as pd

data = pd.read_csv('./TX00.csv')

close = []

for i in range(0, len(data), 30):
    close.append(data.iat[i, 4])



print('5MA: %d' % ma(close[-5:]))
print('10MA: %d' % ma(close[-10:]))
