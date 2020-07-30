import datetime
import json
import requests
import pandas as pd
from io import StringIO
from pprint import pprint as print

'''
Parameter Codes: 

Particulate Matter 2.5 - 88101
Particulate Matter 10 - 85101
Nitrogen Dioxide - 42602
Carbon Monoxide - 42101
Ozone - 44201
Sulfur Dioxide - 42401
'''



def county_air_pollution(parameter: str, start_date: str, end_date: str, state: str, county: str, email='nathandai2000@gmail.com', key='ambergazelle37') -> dict:
    """finds data on the air pollution of a county in a given time frame

    Args:
        parameter (str): parameter code of air pollutant
        start_date (str): YYYYMMDD inclusive
        end_date (str): YYYYMMDD inclusive
        state (str): state code
        county (str): county code
        email (str, optional): must register email for API use. Defaults to 'nathandai2000@gmail.com'.
        key (str, optional): will receive key after email is registered. Defaults to 'ambergazelle37'.

    Returns:
        dict: dictionary of all data in url
    """

    url = f'https://aqs.epa.gov/data/api/dailyData/byCounty?email={email}&key={key}&param={parameter}&bdate={start_date}&edate={end_date}&state={state}&county={county}'

    data = json.loads(requests.get(url).text)

    return data['Data']

def county_average(data: dict) -> pd.DataFrame:
    """returns the average air pollution of each day of a county over one or several days

    Args:
        data (dict): data dictionary excluding header

    Returns:
        pd.DataFrame: arithmetic mean and local date
    """

    return pd.DataFrame([[measurement['arithmetic_mean'], measurement['date_local']] for measurement in data], columns=['arithmetic_mean', 'date_local']).groupby('date_local').mean()
    
if __name__ == '__main__':

    start_date = datetime.date(2020, 3, 1)
    end_date = datetime.date(2020, 3, 2)

    url = 'https://aqs.epa.gov/data/api/dailyData/byCounty?email=nathandai2000@gmail.com&key=ambergazelle37&param=88502&bdate=20200101&edate=20200601&state=06'
    url = 'https://aqs.epa.gov/data/api/dailyData/byCounty?email=nathandai2000@gmail.com&key=test&param=88101&bdate=20160101&edate=20160228&state=37&county=183'
    url = 'https://aqs.epa.gov/data/api/dailyData/byCounty?email=nathandai2000@gmail.com&key=ambergazelle37&param=88101&bdate=20200301&edate=20200302&state=06&county=073' # San Diego, CA 3/1/20 - 3/2/20

    data = county_air_pollution('88101', start_date.strftime('%Y%m%d'), end_date.strftime('%Y%m%d'), '06', '073')
    parsed = county_average(data)

    print(parsed)
