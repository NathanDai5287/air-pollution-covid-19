import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import pandas as pd

from pollution import start_date, start_date_string, end_date, end_date_string, parameters
from pollution import location_to_code, county_average, county_air_pollution
import zip_conversion


def complete_air_pollution(zip_code, parameters, start: str, end: str):
    print(zip_code)
    state, county = zip_conversion.zip_to_location(zip_code)
    state, county = location_to_code(state, county)

    df = pd.DataFrame()
    for parameter in parameters:
        data = county_average(county_air_pollution(
            parameter, start_date_string, end_date_string, state, county), parameters[parameter])

        if (isinstance(data, pd.DataFrame)):
            df = data.join(df, how='outer')

    with open(r'Data Collection\Data\extra\\' + str(zip_code) + '.csv', 'w', newline='') as f:
        f.write(df.to_csv())

    print('Export ' + zip_code + ' Completed')

if __name__ == "__main__":
    with open(r'Data Collection\Apparatus\Docs\zip_codes.csv') as f:
        zip_codes = [i.strip() for i in f.readlines()]

    # complete_air_pollution('92130', parameters)
    # exit(0)

    with ThreadPoolExecutor() as executor:
        _ = [executor.submit(complete_air_pollution, zip_code, parameters, start_date_string, end_date_string) for zip_code in zip_codes[zip_codes.index('60426'):]]
