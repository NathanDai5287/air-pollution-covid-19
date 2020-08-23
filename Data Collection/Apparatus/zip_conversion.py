import pandas as pd


def county_to_zip(county: str, state: str, df: pd.DataFrame) -> list:
    """converts a county and state to a list of zip codes

    Args:
        county (str): name of county
        state (str): state abbreviation
        df (pd.DataFrame): data

    Returns:
        list: list of zip codes
    """

    if (type(county) == float or type(state) == float):
        return []

    county = county.strip()
    
    result = list(df.loc[(df['state'] == state) & (county == df['county'].str.replace(' County', '').str.replace(' City', '')), 'zip'])
    if (result == []):
        print(county + ', ' + state)

    return result

def state_to_abbreviation(state: str, df: pd.DataFrame) -> str:
    """converts a state to its abbreviation

    Args:
        state (str): name of state
        df (regexp, optional): 'Data Collection\Apparatus\Docs\states_and_counties.csv'

    Returns:
        str: abbreviated state name
    """

    return df.loc[df['State Name'] == state.title(), 'State Abbreviation'].iloc[0] 


def zip_to_location(zip_code: str, path=r'Data Collection\Apparatus\Docs\zip_code_database.csv'):
    with open(path) as f:
        df = pd.read_csv(f)[['state', 'county', 'zip']]

    state = df.loc[df['zip'] == int(zip_code), 'state'].iloc[0]
    county = df.loc[df['zip'] == int(zip_code), 'county'].iloc[0][:-7]
    
    with open(r'Data Collection\Apparatus\Docs\states_and_counties.csv') as f:
        df = pd.read_csv(f)[['State Name', 'State Abbreviation']]
    
    state = df.loc[df['State Abbreviation'] == state, 'State Name'].iloc[0]


    return (county, state)


if __name__ == "__main__":
    # print(county_to_zip('St. Tammany', 'Louisiana', df=))
    print(county_to_zip('Tammany', 'LA', df=pd.read_csv(r'Data Collection\Apparatus\Docs\zip_code_database.csv')))
