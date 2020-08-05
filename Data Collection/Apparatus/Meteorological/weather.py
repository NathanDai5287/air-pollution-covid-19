from wwo_hist import retrieve_hist_data
import pandas as pd
import sys
import os
import concurrent.futures
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from top_counties import most_infected

"""
['date_time', 'maxtempC', 'mintempC', 'totalSnow_cm', 'sunHour',
       'uvIndex', 'moon_illumination', 'moonrise', 'moonset', 'sunrise',
       'sunset', 'DewPointC', 'FeelsLikeC', 'HeatIndexC', 'WindChillC',
       'WindGustKmph', 'cloudcover', 'humidity', 'precipMM', 'pressure',
       'tempC', 'visibility', 'winddirDegree', 'windspeedKmph', 'location']
"""


def weather(start_date: str, end_date: str, zip_codes: list, frequency: int, api_key='03347c11e286435386945637203107') -> None:
    """writes to a csv file in the meteorological data directory containing 1 year's worth of meteorological data

    Args:
        start_date (str): start date inclusive; '01-Jan-2020'
        end_date (str): end date inclusive; '02-Jan-2020'
        zip_code (list): list of zip codes
        frequency (int): frequency in hours, usually 24
        api_key (str, optional): obtained from website. Defaults to 'd10267c436334ca88d5222321203007'.
    """

    retrieve_hist_data(api_key, zip_codes, start_date, end_date, frequency,
                       location_label=False, export_csv=True, store_df=True)

    for code in zip_codes:
        data = pd.read_csv(code + '.csv', header=0)

        with open(r'Data Collection\Data\Meteorological\\' + code + '.csv', 'w', newline='') as f:
            f.write(data[['location', 'date_time', 'tempC', 'humidity',
                          'windspeedKmph', 'pressure', 'uvIndex']].to_csv())

        os.remove(code + '.csv')


if __name__ == '__main__':

    API_KEY = '03347c11e286435386945637203107' # max 500 requests per day

    frequency = 24  # hours
    # start_date = '01-JAN-2019'
    start_date = datetime.date(2020, 4, 1)
    str_start_date = '01-APR-2020'
    # end_date = '31-DEC-2019'
    end_date = datetime.date(2020, 5, 31)
    str_end_date = '31-MAY-2020'
    api_key = API_KEY

    # use this to test if all requests have been used
    # weather(start_date, end_date, ['60004'], 24)

    # with concurrent.futures.ThreadPoolExecutor() as executor:
        # executor.submit(weather, str_start_date, str_end_date, ['60001'], 24)
    # exit(0)
    
    zip_codes = most_infected(5, start_date, True)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        _ = [executor.submit(weather, str_start_date, str_end_date, [str(code)], 24) for code in zip_codes]
