import datetime
from io import StringIO

import pandas as pd
import requests

start_date = datetime.date(2020, 2, 1)
end_date = datetime.date(2020, 7, 1)

base_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'

duration = (end_date - start_date).days

days = []
for i in range(duration + 1):
    day = start_date + datetime.timedelta(days=i)
    days.append(day)

data = []
for day in days:
    date = day.strftime('%m-%d-%Y') # string representation of date
    url = base_url + date + '.csv' # url to get
    raw = StringIO(requests.get(url).text) # content of file

    df = pd.read_csv(raw) # pandas DataFrame

    df = df[df['Country/Region'] == 'US'] # filtered to only US

    data.append(df)
