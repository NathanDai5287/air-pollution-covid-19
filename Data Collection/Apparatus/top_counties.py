import numpy as np
import requests
import datetime
import pandas as pd
from io import StringIO
import csv
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
        list: names of counties or zip codes
    """
    
    day = day.strftime('%m-%d-%Y')
    url = f'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{day}.csv'

    df = pd.read_csv(StringIO(requests.get(url).text))
    df = df.loc[df['Country_Region'] == 'US'].sort_values(by='Confirmed', ascending=False) # only US and sort by Confirmed
    df = df.loc[(df['Admin2'] != 'Unassigned') & (df['Province_State'] != 'Puerto Rico')] # remove Unassigned

    locations = list(df.head(n)[['Admin2', 'Province_State']].values)

    df = pd.read_csv(r'Data Collection\Apparatus\Docs\zip_code_database.csv')[['county', 'state', 'zip']]
    df['county'] = df['county'].str.replace(' County','').str.replace(' City','')
    

    if (return_zip):
        state_abbreviation = pd.read_csv(r'Data Collection\Apparatus\Docs\states_and_counties.csv')
        state_abbreviation['State Name'].str.title()

        result = []
        for county, state in locations:
            if (type(county) == str):
                county = county.replace(' County', '').replace(' City', '')
                state = zip_conversion.state_to_abbreviation(state, state_abbreviation)
                result.append([str(code).zfill(5) for code in zip_conversion.county_to_zip(county, state, df)])

        result = [codes for codes in result if codes != []]
        return [y for x in result for y in x]

    else:
        result = []
        for county, state in locations:
            if (type(county) == str):
                county = county.replace(' County', '').replace(' City', '')
                result.append((county, state))

        return result


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
    zip_code = False
    a = top_percent(0.8, date)
    b = most_infected(a, date, zip_code)

    # print(a)
    # exit(0)

    with open('counties.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        # writer.writerows([[i] for i in b])

        if (zip_code):
            for code in b:
                f.write(code + '\n')
        else:
            for location in b:
                writer.writerow(location)
