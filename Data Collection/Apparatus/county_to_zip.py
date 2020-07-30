import pandas as pd
from difflib import get_close_matches


def to_zip(county, path=r'Data Collection\Apparatus\Docs\zip_code_database.csv') -> list:
    """converts a county name to a list of zip codes

    Args:
        county (str): name of county
        path (str, optional): file path to data containing the county names and zip codes. Defaults to r'Data Collection\Apparatus\Docs\zip_code_database.csv'.

    Returns:
        list: list of zip codes
    """

    with open(path) as f:
        df = pd.read_csv(f)[['county', 'zip']]

    counties = [i for i in df['county'] if type(i) == str]

    county_match = get_close_matches(county, counties)

    if (len(county_match) == 0):
        county = get_close_matches(county + ' County', counties)[0]

    return list(df[df['county'] == county]['zip'])

if __name__ == "__main__":
    print(to_zip('san diego'))
