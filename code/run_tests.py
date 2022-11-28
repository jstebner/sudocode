import os
os.chdir(os.path.join(os.getcwd(),'..'))
print(os.getcwd())

from utils import *
from solvers import *
import os
import pandas as pd
from datetime import datetime
def get_time():
    return datetime.now().strftime("%m/%d/%Y %H:%M:%S.%f")

if __name__ == '__main__':
    data = pd.concat([
        pd.read_csv('data/n2.csv'),
        pd.read_csv('data/n3.csv'),
        pd.read_csv('data/n4.csv')
    ])

    cols = ['n','k','pzl','bt_valid','bt_time_ns','bt_recs','bt_space_B','cp_valid','cp_time_ns','cp_recs','cp_space_B']
    with open('out/results.csv', 'a') as file:
        for i, row in data.iloc[2885:].iterrows():
            res_row = [*row]
            for mthd in ['bt','cp']:
                pzl = matrixify(row['pzl'])
                out = solve(mthd, pzl)
                res_row += [*out]
            print(f'{get_time()}: finished {i} ({row["n"]}-{row["k"]})')
            file.write(','.join(list(map(lambda x: str(x), res_row)))+'\n')