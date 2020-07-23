import datetime
from io import StringIO

import pandas as pd
import requests


def us_data(start_date: datetime.date, end_date: datetime.date) -> list:
    """returns United States COVID-19 data

    Args:
        start_date (datetime.date): start date
        end_date (datetime.date): end date

    Returns:
        list: list of pandas DataFrames
    """

    base_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

    duration = (end_date - start_date).days

    days = []
    for i in range(duration + 1):
        day = start_date + datetime.timedelta(days=i)
        days.append(day)

    data = []
    for day in days:
        date = day.strftime('%m-%d-%Y')  # string representation of date
        url = base_url + date + '.csv'  # url to get
        raw = StringIO(requests.get(url).text)  # content of file

        df = pd.read_csv(raw)  # pandas DataFrame

        df = df[df['Country_Region'] == 'US']  # filtered to only US

        data.append(df)

    return data


def new_cases(day: datetime.date, location: str):
    base_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

    yesterday = day - datetime.timedelta(days=1)

    old, new = us_data(yesterday, day)

    old = old.loc[old['Admin2'] == location, 'Confirmed'].iloc[0]
    new = new.loc[new['Admin2'] == location, 'Confirmed'].iloc[0]

    return new - old

if __name__ == "__main__":
    start_date = datetime.date(2020, 2, 1)
    end_date = datetime.date(2020, 7, 1)

    # print(us_data(start_date, end_date))

    print(new_cases(end_date, 'San Diego'))
