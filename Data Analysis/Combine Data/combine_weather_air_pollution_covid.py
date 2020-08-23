import datetime
import pandas as pd
import sys
import os
from pathlib import Path

sys.path.append(os.path.join(os.path.join(os.path.join(os.path.join(os.path.dirname(__file__), '..'), '..'), 'Data Collection'), 'Apparatus'))
# sys.path.append(Path(os.path.dirname(__file__) + '../../Data Collection/Apparatus'))

from zip_conversion import state_to_abbreviation

df = pd.read_csv(Path('Data Analysis/Combine Data/combined_weather_air_pollution_data_by_county.csv'))
covid = pd.read_csv(Path('Data Analysis/Combine Data/combined_air_pollution_covid_data.csv'))[['state', 'county', 'Date', 'Confirmed']]
covid = covid.rename(columns={'Date':'date_local'})

df['date_local'] = [datetime.datetime.strptime('/'.join([i.zfill(2) for i in date.split('/')[:2]] + date.split('/')[-1:]), '%m/%d/%Y').date() for date in df['date_local']]
covid['date_local'] = [datetime.datetime.strptime(date, '%Y-%m-%d').date() for date in covid['date_local']]

df['county'] = [i.replace(' County', '').replace(' City', '') for i in df['county']]

abbreviation_df = pd.read_csv(Path('Data Collection/Apparatus/Docs/states_and_counties.csv'))
covid['state'] = [state_to_abbreviation(i, abbreviation_df) for i in covid['state']]

df.merge(covid, how='outer', on=['state', 'county', 'date_local']).to_csv('final_data.csv', index=False)