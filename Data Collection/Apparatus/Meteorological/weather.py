from wwo_hist import retrieve_hist_data
import pandas as pd
import os
import sys


"""
['date_time', 'maxtempC', 'mintempC', 'totalSnow_cm', 'sunHour',
       'uvIndex', 'moon_illumination', 'moonrise', 'moonset', 'sunrise',
       'sunset', 'DewPointC', 'FeelsLikeC', 'HeatIndexC', 'WindChillC',
       'WindGustKmph', 'cloudcover', 'humidity', 'precipMM', 'pressure',
       'tempC', 'visibility', 'winddirDegree', 'windspeedKmph', 'location']
"""


# api key, hours, start: "01-Jan-2020", end: "01-Jan-2021", ["92130"]
def weather(api_key: str, frequency: int, start_date: str, end_date: str, zip_code: list, location_label=False, export_csv=False, store_df=True) -> pd.DataFrame:
    """returns a pandas DataFrame that contains:
    location, date, average temperature, humidity, wind speed, air pressure, uvIndex

    Args:
        api_key (str): obtained from website; valid for 90 daya
        frequency (int): how frequent the data should be in hours, usually 24
        start_date (str): start date inclusive
        end_date (str): end date inclusive
        zip_code (list): zip code to get data from
        location_label (bool, optional): no clue what this does. Defaults to False.
        export_csv (bool, optional): [description]. Defaults to False.
        store_df (bool, optional): [description]. Defaults to True.

    Returns:
        pd.DataFrame: [description]
    """

    retrieve_hist_data(api_key, zip_code, start_date, end_date, frequency,
                       location_label=location_label, export_csv=export_csv, store_df=store_df)

    data = pd.read_csv(zip_code[0] + '.csv', header=0)
    os.remove(zip_code[0] + '.csv')

    return data[['location', 'date_time', 'tempC', 'humidity', 'windspeedKmph', 'pressure', 'uvIndex']] # choose which to return

if __name__ == '__main__':

    API_KEY = '62c4f496efb147c1b2160953202406'

    frequency = 24  # hours
    start_date = '01-JAN-2020'
    end_date = '01-JAN-2020'
    api_key = API_KEY
    location_list = ['92130'] # list of zip codes to get data from

    data = weather(api_key, frequency, start_date, end_date,
                location_list, store_df=True, export_csv=True)

    with open(r'Data Collection\Data\Meteorological\\' + location_list[0] + '.csv', 'w', newline='') as f:
        f.write(data.to_csv())
