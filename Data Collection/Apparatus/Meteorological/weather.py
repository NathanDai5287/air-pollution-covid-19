from wwo_hist import retrieve_hist_data
import pandas as pd
import os
import sys

API_KEY = '62c4f496efb147c1b2160953202406'

frequency = 24  # hours
start_date = '01-JAN-2020'
end_date = '22-JAN-2020'
api_key = API_KEY
location_list = ['92130'] # list of zip codes to get data from

"""
['date_time', 'maxtempC', 'mintempC', 'totalSnow_cm', 'sunHour',
       'uvIndex', 'moon_illumination', 'moonrise', 'moonset', 'sunrise',
       'sunset', 'DewPointC', 'FeelsLikeC', 'HeatIndexC', 'WindChillC',
       'WindGustKmph', 'cloudcover', 'humidity', 'precipMM', 'pressure',
       'tempC', 'visibility', 'winddirDegree', 'windspeedKmph', 'location']
"""


# api key, hours, start: "01-Jan-2020", end: "01-Jan-2021", ["92130"]
def weather(api_key: str, frequency: int, start_date: str, end_date: str, zip_code: list, location_label=False, export_csv=False, store_df=True) -> pd.DataFrame:
    """
    returns a pandas DataFrame that contains:
    location, date, average temperature, humidity, wind speed, air pressure, uvIndex
    """
    
    retrieve_hist_data(api_key, zip_code, start_date, end_date, frequency,
                       location_label=location_label, export_csv=export_csv, store_df=store_df)

    path = str(os.path.join(os.path.join(os.path.join(
        os.path.dirname(__file__), '..'), '..'), str(zip_code[0]) + '.csv'))

    data = pd.read_csv(path, header=0)

    os.remove(path)

    return data[['location', 'date_time', 'tempC', 'humidity', 'windspeedKmph', 'pressure', 'uvIndex']] # choose which to return


data = weather(api_key, frequency, start_date, end_date,
               location_list, store_df=True, export_csv=True)

with open(r'Data Collection\Data\\' + location_list[0], 'w', newline='') as f:
    f.write(data.to_csv())