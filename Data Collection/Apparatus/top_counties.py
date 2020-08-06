import numpy as np
import requests
import datetime
import pandas as pd
from io import StringIO
from difflib import get_close_matches
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import zip_conversion

def most_infected(n: int, day: datetime.date, return_zip: bool) -> list:
    """returns a list of the most infected counties

    Args:
        n (int): top n counties will be returned
        day (datetime.date): date to observe counties

    Returns:
        list: names of counties
    """
    
    day = day.strftime('%m-%d-%Y')
    url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{day}.csv'

    df = pd.read_csv(StringIO(requests.get(url).text))
    df = df.loc[df['Country_Region'] == 'US'].sort_values(by='Confirmed', ascending=False)

    return [y for x in [zip_conversion.county_to_zip(county, state) for county, state in list(df.head(n)[['Admin2', 'Province_State']].values)] for y in x] if return_zip else [(county, state) for county, state in list(df.head(n)[['Admin2', 'Province_State']].values)]


def top_percent(n: float, day: datetime.date) -> int:
    """how many counties make up n percent of cases

    Args:
        n (float): fraction of total cases
        day (datetime.date): day to check

    Returns:
        int: this many counties makes up n of the cases
    """

    day = day.strftime('%m-%d-%Y')
    url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{day}.csv'

    df = pd.read_csv(StringIO(requests.get(url).text))
    df = df.loc[df['Country_Region'] == 'US'].sort_values(by='Confirmed', ascending=False)

    confirmed = list(df['Confirmed'])
    reach = sum(confirmed) * n
    top = list(np.cumsum(confirmed) >= reach).index(True)

    return top

if __name__ == "__main__":
    date = datetime.date(2020, 4, 1)
    a = top_percent(0.8, date)
    b = most_infected(a, date, False)

    print(len(b))
