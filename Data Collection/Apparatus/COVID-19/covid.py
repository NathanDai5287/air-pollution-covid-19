import datetime
from io import StringIO
import concurrent.futures
import os
import sys

import pandas as pd
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from top_counties import most_infected


def days_between(start_date: datetime.date, end_date: datetime.date) -> list:
    """returns a list of datetime date objects for each day between the start and end dates

    Args:
        start_date (datetime.date): start date
        end_date (datetime.date): end date

    Returns:
        list: list of date objects
    """
    return [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]


def us_data(start_date: datetime.date, end_date: datetime.date) -> list:
    """returns United States COVID-19 data

    Args:
        start_date (datetime.date): start date
        end_date (datetime.date): end date

    Returns:
        list: list of pandas DataFrames; one DataFrame for each day
    """

    base_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

    days = days_between(start_date, end_date)

    data = []
    for day in days:
        date = day.strftime('%m-%d-%Y')  # string representation of date
        url = base_url + date + '.csv'  # url to get
        raw = StringIO(requests.get(url).text)  # content of file

        df = pd.read_csv(raw)  # pandas DataFrame

        try:
            df = df[df['Country_Region'] == 'US']  # filtered to only US
        except KeyError:
            df = df[df['Country/Region'] == 'US']  # filtered to only US

        data.append(df)

    return data


# def new_cases(day: datetime.date, location: str) -> int:
#     """returns the number of new cases on any day and in any city in the United States

#     Args:
#         day (datetime.date): day to get new cases
#         location (str): county to get new cases

#     Returns:
#         int: new cases
#     """

#     yesterday = day - datetime.timedelta(days=1)

#     old, new = us_data(yesterday, day)

#     try:
#         old = old.loc[old['Admin2'] == location, 'Confirmed'].iloc[0]
#     except KeyError:
#         old = 0

#     try:
#         new = new.loc[new['Admin2'] == location, 'Confirmed'].iloc[0]
#     except KeyError:
#         return 0

#     return new - old

# def daily_new_cases(start_date: datetime.date, end_date: datetime.date, location: str) -> list:
#     """returns the daily new cases data for a specific county

#     Args:
#         start_date (datetime.date): start date
#         end_date (datetime.date): end date
#         location (str): county

#     Returns:
#         list: list of integers containing daily new cases data
#     """
#     cases = [new_cases(day, location)
#              for day in days_between(start_date, end_date)]
#     return cases


def confirmed_cases(day: datetime.date, county: str, state: str) -> int:
    day = day.strftime('%m-%d-%Y')
    url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{day}.csv'

    df = pd.read_csv(StringIO(requests.get(url).text))
    df = df.loc[df['Country_Region'] == 'US']
    df = df.loc[df['Province_State'] == state]
    df = df[['Admin2', 'Confirmed']]

    return int(df.loc[df['Admin2'] == county]['Confirmed'].iloc[0])


def daily_confirmed_cases_complete(start_date, end_date, county, state):
    cases = {}
    for day in days_between(start_date, end_date):
        cases[day] = confirmed_cases(day, county, state)

    cases = pd.DataFrame([[key, value] for key, value in cases.items()])
    cases.columns = ['Date', 'Confirmed']
    cases.set_index('Date', inplace=True)

    with open(r'Data Collection\Data\COVID-19\\' + state.replace(' ', '-') + '_' + county.replace(' ', '-') + '.csv', 'w', newline='') as f:
        print(county + ', ' + state + ' export complete')
        f.write(cases.to_csv())

if __name__ == "__main__":
    start_date = datetime.date(2020, 3, 31)
    end_date = datetime.date(2020, 5, 31)

    with open(r'Data Collection\Apparatus\Docs\counties.csv') as f:
        locations = list(map(tuple, [(''.join([i for i in j if i.isalpha() or i == ',' or i == ' ']).split(', ')) for j in f.readlines()]))

    with concurrent.futures.ThreadPoolExecutor() as executor:
        _ = [executor.submit(daily_confirmed_cases_complete, start_date, end_date, county, state) for county, state in locations[::-1]]
    exit(0)

    daily_confirmed_cases_complete(start_date, end_date, 'New York City', 'New York')


    for county, state in most_infected(5, start_date, False):
        cases = {}
        for day in days_between(start_date, end_date):
            cases[day] = confirmed_cases(day, county, state)

        cases = pd.DataFrame([[key, value] for key, value in cases.items()])
        cases.columns = ['Date', 'Confirmed']
        cases.set_index('Date', inplace=True)
        
        with open(r'Data Collection\Data\COVID-19\\' + county + '.csv', 'w', newline='') as f:
            f.write(cases.to_csv())


