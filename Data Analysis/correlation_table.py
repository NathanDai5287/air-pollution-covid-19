import pandas as pd

df = pd.read_csv('Data Analysis\combined_data.csv')
df.drop(['date_local'], axis=1)

with open('Data Analysis\correlation_table.csv', 'w', newline='') as f:
    f.write(df.corr('spearman').to_csv())