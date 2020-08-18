import pandas as pd

pollution = pd.read_csv(r'Data Analysis\Air Pollution\county_air_pollution.csv')
pollution.rename(columns={'date_local': 'Date'}, inplace=True)
covid = pd.read_csv(r'Data Analysis\COVID-19\county_covid-19_data.csv')
covid['New Confirmed'] = covid['Confirmed'].diff().shift(-1)

df = covid.merge(pollution, on=['Date', 'state', 'county'], how='outer')
df.to_csv(r'Data Analysis\combined_air_pollution_log_covid_data.csv')