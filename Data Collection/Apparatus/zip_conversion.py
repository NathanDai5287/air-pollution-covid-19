import pandas as pd
from difflib import get_close_matches


def county_to_zip(county: str, state: str, path=r'Data Collection\Apparatus\Docs\zip_code_database.csv') -> list:
    """converts a county name to a list of zip codes

    Args:
        county (str): name of county
        path (str, optional): file path to data containing the county names and zip codes. Defaults to r'Data Collection\Apparatus\Docs\zip_code_database.csv'.

    Returns:
        list: list of zip codes
    """

    with open(path) as f:
        df = pd.read_csv(f)[['county', 'state', 'zip']]

    counties = [i for i in df['county'] if type(i) == str]
    county_match = get_close_matches(county, counties)

    states = list(df['state'].unique())
    state = get_close_matches(state_to_abbreviation(state), states)[0]

    if (len(county_match) == 0):
        county = get_close_matches(county + ' County', counties)[0]

    return list(df.loc[(df['state'] == state) & (df['county'] == county), 'zip'])

def state_to_abbreviation(state: str, path=r'Data Collection\Apparatus\Docs\states_and_counties.csv') -> str:
    """converts a state to its abbreviation

    Args:
        state (str): name of state
        path (regexp, optional): path to database. Defaults to r'Data Collection\Apparatus\Docs\states_and_counties.csv'.

    Returns:
        str: abbreviated state name
    """

    with open(path) as f:
        df = pd.read_csv(f)

    states = list(df['State Name'].unique())
    state = get_close_matches(state, states)[0]

    return df.loc[df['State Name'] == state, 'State Abbreviation'].iloc[0] 


def zip_to_location(zip_code: str, path=r'Data Collection\Apparatus\Docs\zip_code_database.csv'):
    with open(path) as f:
        df = pd.read_csv(f)[['state', 'county', 'zip']]

    state = df.loc[df['zip'] == int(zip_code), 'state'].iloc[0]
    county = df.loc[df['zip'] == int(
        zip_code), 'county'].iloc[0].strip(' County')
    
    with open(r'Data Collection\Apparatus\Docs\states_and_counties.csv') as f:
        df = pd.read_csv(f)[['State Name', 'State Abbreviation']]
    
    state = df.loc[df['State Abbreviation'] == state, 'State Name'].iloc[0]


    return (state, county)


if __name__ == "__main__":
    print(county_to_zip('sn diego', 'acliforia'))
