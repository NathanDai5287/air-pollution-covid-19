import json
import pandas as pd

import zip_conversion

with open(r'Data Collection\Apparatus\Docs\counties.csv') as f:
    locations = [tuple(i.strip().split(',')) for i in f.readlines()]

zip_codes = []
dictionary = {}
state_abbreviation = pd.read_csv(r'Data Collection\Apparatus\Docs\states_and_counties.csv')
zip_code_data = pd.read_csv(r'Data Collection\Apparatus\Docs\zip_code_database.csv')
for location in locations:
    zip_code = zip_conversion.county_to_zip(location[0], zip_conversion.state_to_abbreviation(location[1], state_abbreviation), zip_code_data)
    zip_codes += zip_code
    dictionary[str(location)] = str(zip_code).zfill(5)

with open(r'zip.json', 'w') as f:
    f.write(json.dumps(dictionary))

with open(r'zip.csv', 'w') as f:
    for code in zip_codes:
        f.write(str(code).zfill(5) + '\n')