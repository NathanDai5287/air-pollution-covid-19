import sys
import os

sys.path.append(os.path.join(os.path.join(os.path.join(os.path.join(os.path.join(os.path.dirname(__file__), '..'), '..'), 'Data Collection'), 'Data'), 'Meteorological'))

import json
from typing import Union, Tuple
import pandas as pd
from concurrent.futures import ProcessPoolExecutor

def zip_data_to_county(location: Union[str, Tuple[str, str]], filename: list, measurements: list, data_category: str, zip_data: bool) -> pd.DataFrame:
    if (zip_data):
        county, state = (''.join([i for i in location if i.isalpha() or i == ',' or i == ' ']).split(', '))
        list_df = [pd.read_csv(r'Data Collection\Data\\' + data_category + r'\\' + str(code) + '.csv') for code in filename]   
    else:
        county, state = location
        # list_df = [pd.read_csv(location) for location in ]

    df = pd.DataFrame(columns=measurements)
    for i, dataframe in enumerate(list_df):
        if (not(dataframe.empty)):
            df = df.merge(dataframe, how='outer', on='date_time', suffixes=(None, '_' + str(i)))
    
    for measurement in measurements[1:]:
        headers = [column for column in df.columns if measurement in column]

        df[measurement] = df[headers].mean(axis=1)
    
    df = df[measurements]
    df['state'] = state
    df['county'] = county

    return df

def combined_zip_data_to_county(df: pd.DataFrame):
    return pd.DataFrame(df.groupby(['state', 'county', 'date_local']).mean()).drop(columns='location')

df = combined_zip_data_to_county(pd.read_csv(r'Data Analysis\Combine Data\combined_weather_air_pollution_data.csv'))    
df.to_csv(r'Data Analysis\Combine Data\combined_weather_air_pollution_data_by_county.csv')
if __name__ == "__main__":
    with open(r'Data Collection\Apparatus\Docs\county_zip_map.json') as f:
        zip_code_dict = json.load(f)

    data_category = 'Meteorological'
    # measurements = ['date_time', 'tempC', 'humidity', 'windspeedKmph', 'pressure', 'uvIndex']
    measurements = ['location', 'date_local', 'PM2.5', 'O3', 'SO2', 'NO2', 'PM10', 'CO', 'tempC', 'humidity', 'windspeedKmph', 'pressure', 'uvIndex']

    with ProcessPoolExecutor() as executor:
        list_df = [executor.submit(zip_data_to_county, location, [str(code).zfill(5) for code in zip_codes], measurements, data_category, True) for location, zip_codes in list(zip_code_dict.items())[:3]]

    df = pd.DataFrame(columns=['state', 'county'] + measurements)
    for dataframe in list_df:
        df = df.append(dataframe.result(), ignore_index=True)
    
    df = df[['county', 'state'] + measurements]
    df.to_csv(r'Data Analysis\\' + data_category + r'\\' + 'county_' + data_category.lower() + '_data.csv', index=False)
