import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from zip_data_to_county import zip_data_to_county

import glob
import json
import pandas as pd
from concurrent.futures import ProcessPoolExecutor

if __name__ == "__main__":
    data_category = 'COVID-19'
    measurements = ['Date', 'Confirmed']

    # a = [zip_data_to_county(location[location.index('COVID-19') + 9:-4].split('_'), location, measurements, data_category, False) for location in glob.glob(r'Data Collection\Data\COVID-19\*.csv')]

    # with ProcessPoolExecutor() as executor:
        # list_df = [executor.submit(zip_data_to_county, location[location.index('COVID-19') + 9:].split('_'), location[location.index('COVID-19') + 9:], measurements, data_category, False) for location in glob.glob(r'Data Collection\Data\COVID-19\*.csv')]
    # print(a[0])

    df = pd.DataFrame(columns=['state', 'county'] + measurements)
    for path in glob.glob(r'Data Collection\Data\COVID-19\*.csv'):
        dataframe = pd.read_csv(path)
        state, county = path[path.index('COVID-19') + 9:-4].split('_')
        state, county = state.replace('-', ' '), county.replace('-', ' ')
        dataframe['state'] = state
        dataframe['county'] = county

        df = df.append(dataframe, ignore_index=True)
    
    df = df[['county', 'state'] + measurements]
    df.to_csv(r'Data Analysis\\' + data_category + r'\\' + 'county_' + data_category.lower() + '_data.csv', index=False)
