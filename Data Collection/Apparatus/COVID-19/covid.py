import datetime
from io import StringIO

import pandas as pd
import requests


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


def new_cases(day: datetime.date, location: str) -> int:
    """returns the number of new cases on any day and in any city in the United States

    Args:
        day (datetime.date): day to get new cases
        location (str): county to get new cases

    Returns:
        int: new cases
    """
    base_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

    yesterday = day - datetime.timedelta(days=1)

    old, new = us_data(yesterday, day)

    old = old.loc[old['Admin2'] == location, 'Confirmed'].iloc[0]
    new = new.loc[new['Admin2'] == location, 'Confirmed'].iloc[0]

    return new - old

def daily_new_cases(start_date: datetime.date, end_date: datetime.date, location: str) -> list:
    """returns the daily new cases data for a specific county

    Args:
        start_date (datetime.date): start date
        end_date (datetime.date): end date
        location (str): county

    Returns:
        list: list of integers containing daily new cases data
    """
    cases = [new_cases(day, location) for day in days_between(start_date, end_date)]

if __name__ == "__main__":
    start_date = datetime.date(2020, 2, 1)
    end_date = datetime.date(2020, 7, 1)

    print(us_data(start_date, end_date))

    print(new_cases(end_date, 'San Diego'))
