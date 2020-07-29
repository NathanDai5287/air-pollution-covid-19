import pandas as pd
from difflib import get_close_matches


def search(data: pd.DataFrame, state: str, county: str) -> tuple:
    """searches for a state and county and outputs their codes

    Args:
        data (pd.DataFrame): dataframe to search in
        state (str): name of state
        county (str): name of county

    Returns:
        tuple: (state code, county code) both padded with zeros
    """

    states = data['State Name'].unique()
    counties = data['County Name'].unique()

    # smart search
    state = get_close_matches(state, states)[0]
    county = get_close_matches(county, counties)[0]
    
    state_code = data[data['State Name'] == state]['State Code'].iloc[0]
    county_code = data[data['County Name'] == county]['County Code'][data['State Name'] == state].iloc[0]

    return str(state_code).zfill(2), str(county_code).zfill(3)

if __name__ == '__main__':
    with open(r'Data Collection\Apparatus\Air Pollution\states_and_counties.csv') as f:
        data = pd.read_csv(f).drop('EPA Region', axis=1)
    
    print(search(data, 'california', 'san diego'))
