import pandas as pd
from pathlib import Path
import datetime

df = pd.read_csv(Path('Data Collection/Data/final_data.csv'), parse_dates=['date_local'])
# df['date_local'] = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in df['date_local']]
df.sort_values(by=['date_local'], inplace=True)
df['New Cases'] = df.groupby(['state', 'county'])['Confirmed'].diff()
df.sort_values(by=['state', 'county', 'date_local'], inplace=True)
df.to_csv('delete.csv', index=False)