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


# api key, hours, start: "01-Jan-2020", end: "01-Jan-2021", ["92130"]
def weather(start_date: str, end_date: str, zip_code: list, frequency: int, location_label=False, export_csv=True, store_df=True, api_key='62c4f496efb147c1b2160953202406') -> pd.DataFrame:
    """returns a pandas DataFrame that contains:
    location, date, average temperature, humidity, wind speed, air pressure, uvIndex

    Args:
        start_date (str): start date inclusive; '01-Jan-2020'
        end_date (str): end date inclusive; '02-Jan-2020'
        zip_code (list): list of zip codes
        frequency (int): frequency in hours, usually 24
        location_label (bool, optional): no clue. Defaults to False.
        export_csv (bool, optional): keep as True. Defaults to True.
        store_df (bool, optional): keep as True. Defaults to True.
        api_key (str, optional): obtained from website; valid for 90 days. Defaults to '62c4f496efb147c1b2160953202406'.

    Returns:
        pd.DataFrame: contains data listed above
    """

    retrieve_hist_data(api_key, [zip_code], start_date, end_date, frequency,
                       location_label=location_label, export_csv=True, store_df=store_df)

    for code in zip_code:
        data = pd.read_csv(code + '.csv', header=0)
        os.remove(code + '.csv')

    print(f'deleted file {zip_code}.csv')

    return data[['location', 'date_time', 'tempC', 'humidity', 'windspeedKmph', 'pressure', 'uvIndex']] # choose which to return

def complete_weather_procces(start_date: str, end_date: str, zip_code: list, frequency: int, location_label=False, export_csv=True, store_df=True, api_key='62c4f496efb147c1b2160953202406') -> bool:
    data = weather(start_date, end_date, zip_code, frequency)

    for i in data:
        with open(r'Data Collection\Data\Meteorological\\' + zip_code[i] + '.csv', 'w', newline='') as f:
            f.write(data.to_csv())
            print(f'write {zip_code}')
    
    return True

if __name__ == '__main__':

    API_KEY = '62c4f496efb147c1b2160953202406'

    frequency = 24  # hours
    start_date = '01-JAN-2019'
    # end_date = '31-DEC-2019'
    end_date = '31-JAN-2019'
    api_key = API_KEY
    location_list = ['92130', '92121'] # list of zip codes to get data from

    with open(r'Data Collection\Apparatus\Docs\all_zip_codes.csv') as f:
        all_zip_codes = [code.strip() for code in f.readlines()]

    complete_weather_procces(start_date, end_date, location_list, 24)
