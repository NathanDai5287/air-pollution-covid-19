import datetime
import json
from numpy.core.fromnumeric import mean
import requests
import pandas as pd
from io import StringIO
from pprint import pprint as print
from difflib import get_close_matches
import time

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

    if (data['Header'][0]['status'] == 'No data matched your selection'):
        return False

    return data['Data']


def county_average(data: dict, pollutant: str) -> pd.DataFrame:
    """returns the average air pollution of each day of a county over one or several days

    Args:
        data (dict): data dictionary excluding header; obtained from county_air_pollution()

    Returns:
        pd.DataFrame: arithmetic mean and local date
    """

    if (data == False):
        return False
    return pd.DataFrame([[measurement['arithmetic_mean'], measurement['date_local']] for measurement in data], columns=[pollutant, 'date_local']).groupby('date_local').mean()


def location_to_code(state: str, county: str, path=r'Data Collection\Apparatus\Docs\states_and_counties.csv') -> tuple:
    """searches for a state and county and outputs their codes

    Args:
        state (str): name of state
        county (str): name of county that is in the state
        path (str, optional): path to csv file containg state and county codes. Defaults to r'Data Collection\Apparatus\Docs\states_and_counties.csv'.

    Returns:
        tuple: (state code: str, county code: str) both padded with zeros
    """

    with open(path) as f:
        data = pd.read_csv(f).drop('EPA Region', axis=1)

    states = data['State Name'].unique()
    state = get_close_matches(state, states)[0]

    counties = data.loc[data['State Name'] == state]['County Name']
    county = get_close_matches(county, counties)[0]

    state_code = data[data['State Name'] == state]['State Code'].iloc[0]
    county_code = data.loc[(data['State Name'] == state) & (
        data['County Name'] == county)]['County Code'].iloc[0]

    return str(state_code).zfill(2), str(county_code).zfill(3)


def to_zip(county, path=r'Data Collection\Apparatus\Docs\zip_code_database.csv') -> list:
    """converts a county name to a list of zip codes

    Args:
        county (str): name of county
        path (str, optional): file path to data containing the county names and zip codes. Defaults to r'Data Collection\Apparatus\Docs\zip_code_database.csv'.

    Returns:
        list: list of zip codes
    """

    with open(path) as f:
        df = pd.read_csv(f)[['county', 'zip']]

    counties = [i for i in df['county'] if type(i) == str]

    county_match = get_close_matches(county, counties)

    if (len(county_match) == 0):
        county = get_close_matches(county + ' County', counties)[0]

    return list(df[df['county'] == county]['zip'])


def zip_to_location(zip_code: str, path=r'Data Collection\Apparatus\Docs\zip_code_database.csv'):
    with open(path) as f:
        df = pd.read_csv(f)[['state', 'county', 'zip']]

    state = df.loc[df['zip'] == int(zip_code), 'state'].iloc[0]
    county = df.loc[df['zip'] == int(
        zip_code), 'county'].iloc[0].strip(' County')
    
    with open(r'Data Collection\Apparatus\Docs\states_and_counties.csv') as f:
        df = pd.read_csv(f)[['State Name', 'State Abbreviation']]
    
    state = df.loc[df['State Abbreviation'] == state, 'State Name'].iloc[0]


    return (state, county)


def days_between(start_date: datetime.date, end_date: datetime.date) -> list:
    """returns a list of datetime date objects for each day between the start and end dates

    Args:
        start_date (datetime.date): start date
        end_date (datetime.date): end date

    Returns:
        list: list of date objects
    """
    return [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]


if __name__ == '__main__':
    parameters = {'42101': 'CO',
                '42401': 'SO2',
                '42602': 'NO2',
                '44201': 'O3',
                '85101': 'PM10',
                '88101': 'PM2.5'}

    with open(r'Data Collection\Apparatus\Docs\all_zip_codes.csv') as f:
        all_zip_codes = [code.strip().strip(',') for code in f.readlines()]

    # start_date = datetime.date(2019, 1, 1).strftime('%Y%m%d')
    start_date = datetime.date(2019, 1, 1).strftime('%Y%m%d')
    # end_date = datetime.date(2019, 12, 31).strftime('%Y%m%d')
    end_date = datetime.date(2019, 1, 6).strftime('%Y%m%d')


    for zip_code in all_zip_codes:
        state, county = zip_to_location(zip_code)
        state, county = location_to_code(state, county)

        df = pd.DataFrame()
        for parameter in parameters.keys():
            data = county_average(county_air_pollution(
                parameter, start_date, end_date, state, county), parameters[parameter])

            if (isinstance(data, pd.DataFrame)):
                df = data.join(df, how='outer')

        with open(r'Data Collection\Data\Air Pollution\\' + zip_code + '.csv', 'w', newline='') as f:
            f.write(df.to_csv())
