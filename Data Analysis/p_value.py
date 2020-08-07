import pandas as pd
import scipy.stats
import numpy as np
from itertools import combinations

data = pd.read_csv(r'Data Analysis\combined_data.csv').drop('date_local', axis=1)

pm = np.array(data['PM2.5'])
ozone = np.array(data['O3'])
nitrogendioxide = np.array(data['NO2'])

# r, p = scipy.stats.spearmanr(pm, nitrogendioxide)
# print(r, p)
# exit(0)

df = pd.DataFrame(columns=data.columns, index=data.columns)
for i in combinations(df.columns, 2):
    a = np.array(data[i[0]])
    b = np.array(data[i[1]])
    _, p = scipy.stats.spearmanr(a, b)

    df[i[0]][i[1]] = p

with open(r'Data Analysis\p_value.csv', 'w', newline='') as f:
    f.write(df.to_csv())
