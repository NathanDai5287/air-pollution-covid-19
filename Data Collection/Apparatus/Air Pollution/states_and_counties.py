import pandas as pd
from difflib import get_close_matches


def search(state: str, county: str, path=r'Data Collection\Apparatus\Docs\states_and_counties.csv') -> tuple:
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
    county_code = data.loc[(data['State Name'] == state) & (data['County Name'] == county)]['County Code'].iloc[0]
   

    return str(state_code).zfill(2), str(county_code).zfill(3)

if __name__ == '__main__':    
    print(search('oregon', 'washington'))
