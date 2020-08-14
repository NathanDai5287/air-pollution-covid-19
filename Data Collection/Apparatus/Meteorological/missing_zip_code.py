import glob

def zip_codes_to_go(target: list, zip_code: list) -> list:
    """finds the zip codes that haven't been used

    Args:
        target (list): the list of zip codes that you want
        zip_code (list): the list of zip codes that you already have

    Returns:
        list: list of zip codes that you still need
    """
    
    combined = target + zip_code

    for code in target:
        if (combined.count(code) > 1):
            combined = [i for i in combined if i != code]
    
    return sorted(combined)


if __name__ == "__main__":
    zip_codes = [zip_code[zip_code.find('Meteorological\\') + 15:zip_code.find('.csv')] for zip_code in glob.glob(r'Data Collection\Data\Meteorological\*.csv')]
    # zip_codes = [zip_code for zip_code in glob.glob(r'Data Collection\Data\Meteorological\*.csv')]

    with open(r'Data Collection\Apparatus\Docs\zip_codes_to_use.csv') as f:
        target = [zip_code.strip(',\n') for zip_code in f.readlines()]

    with open(r'Data Collection\Apparatus\Docs\missing.csv', 'w') as f:
        f.writelines('\n'.join(zip_codes_to_go(target, zip_codes)))
