import os
from utils import *
import pandas as pd
from time import process_time_ns
from datetime import datetime

def get_time():
    return datetime.now().strftime("%m/%d/%Y %H:%M:%S.%f")

if __name__ == '__main__':
    os.chdir(os.path.join(os.path.dirname(__file__), '..')) # move to root of project
    
    # cols = ['n','k','pzl']

    n = 5
    with open(f'./data/n{n}.csv', 'w') as file:
        file.write("n,k,pzl\n")
        for k in range(1, 52*n-91): # formula for largest k, pretty much chosen arbitrarily
            for _ in range(30): # 30 because statistical significance or smthn like that
                print(f"{get_time()}: making n:{n} k:{k}")
                start = process_time_ns()
                
                pzl, sln = make_puzzle(n, k)
                # print(pzl)
                
                end = process_time_ns()
                print(f"{get_time()}: finished, took {round((end-start)/(10e9), 4)} s")
                file.write(f"{n},{k},{pzl}\n")
            # quit()
                    

    # df = pd.DataFrame(data, columns=cols)
    # print(df)
    # df.to_csv('./data/n3.csv', index=False)
    
    # df = pd.read_csv('./data/n3.csv')
    # print(df)