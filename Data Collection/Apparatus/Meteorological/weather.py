from wwo_hist import retrieve_hist_data
import pandas as pd
import os
import concurrent.futures

"""
['date_time', 'maxtempC', 'mintempC', 'totalSnow_cm', 'sunHour',
       'uvIndex', 'moon_illumination', 'moonrise', 'moonset', 'sunrise',
       'sunset', 'DewPointC', 'FeelsLikeC', 'HeatIndexC', 'WindChillC',
       'WindGustKmph', 'cloudcover', 'humidity', 'precipMM', 'pressure',
       'tempC', 'visibility', 'winddirDegree', 'windspeedKmph', 'location']
"""


def weather(start_date: str, end_date: str, zip_codes: list, frequency: int, api_key='272f03c5e20641598f4200659203007') -> None:
    """writes to a csv file in the meteorological data directory containing 1 year's worth of meteorological data

    Args:
        start_date (str): start date inclusive; '01-Jan-2020'
        end_date (str): end date inclusive; '02-Jan-2020'
        zip_code (list): list of zip codes
        frequency (int): frequency in hours, usually 24
        api_key (str, optional): [description]. Defaults to '272f03c5e20641598f4200659203007'.
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

    API_KEY = '272f03c5e20641598f4200659203007' # max 500 requests per day

    frequency = 24  # hours
    start_date = '01-JAN-2019'
    end_date = '31-DEC-2019'
    # end_date = '02-JAN-2019'
    api_key = API_KEY

    with open(r'Data Collection\Apparatus\Docs\all_zip_codes.csv') as f:
        all_zip_codes = [code.strip().strip(',') for code in f.readlines()]

    # use this to test if all requests have been used
    # weather(start_date, end_date, all_zip_codes[429:430], 24)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        _ = [executor.submit(weather, start_date, end_date, [code], 24) for code in all_zip_codes]
