import pandas as pd

df = pd.read_csv(r'combined_weather_air_pollution_data.csv')

database = pd.read_csv(r'Data Collection\Apparatus\Docs\zip_code_database.csv')[['zip', 'county', 'state']]
zip_map = dict(zip(database.zip, database.county))
state_map = dict(zip(database.zip, database.state))

df['county'] = [zip_map[df['location'].iloc[i]] for i in range(len(df))]
df['state'] = [state_map[df['location'].iloc[i]] for i in range(len(df))]
df = df[['state', 'county', 'location', 'date_local', 'PM2.5', 'O3', 'SO2', 'NO2', 'PM10', 'CO', 'tempC', 'humidity', 'windspeedKmph', 'pressure', 'uvIndex']]
df.to_csv(r'combined_weather_air_pollution_data.csv', index=False)
