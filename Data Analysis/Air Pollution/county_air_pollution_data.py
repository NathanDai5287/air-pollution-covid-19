import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from zip_data_to_county import zip_data_to_county
import pandas as pd
import json
from concurrent.futures import ProcessPoolExecutor

with open(r'Data Collection\Apparatus\Docs\county_zip_map.json') as f:
    zip_code_dict = json.load(f)

data_category = 'Meteorological'
measurements = ['date_time', 'tempC', 'humidity', 'windspeedKmph', 'pressure', 'uvIndex']

with ProcessPoolExecutor() as executor:
    list_df = [executor.submit(zip_data_to_county, location, [str(code).zfill(5) for code in zip_codes], measurements, data_category) for location, zip_codes in zip_code_dict.items()]

df = pd.DataFrame(columns=['state', 'county'] + measurements)
for dataframe in list_df:
    df = df.append(dataframe.result(), ignore_index=True)

df = df[['county', 'state'] + measurements]
df.to_csv(r'Data Analysis\\' + data_category + r'\\' + 'county_' + data_category.lower().replace(' ', '_') + '_data.csv', index=False)
