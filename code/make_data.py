import os
from utils import *
import pandas as pd
from time import time

if __name__ == '__main__':
    os.chdir(os.path.join(os.path.dirname(__file__), '..'))
    
    cols = ['n','k','pzl']
    data = []

    for n in range(2, 7):
        for k in range(1, 65):
            for _ in range(40):
                pass

    # df = pd.DataFrame(data, columns=cols)
    # print(df)
    # df.to_csv('./data/n3.csv', index=False)
    
    # df = pd.read_csv('./data/n3.csv')
    # print(df)