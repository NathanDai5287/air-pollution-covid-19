import pandas as pd
import glob
import concurrent.futures

def correlation(pollution_path, meteorological_path) -> pd.DataFrame:
    pollution = pd.read_csv(pollution_path)
    meteorological = pd.read_csv(meteorological_path)

    meteorological.rename(columns={'date_time':'date_local'}, inplace = True) 

    df = pollution.merge(meteorological, how='outer', on='date_local')
    del df['Unnamed: 0']
    columns = list(df.columns)
    location = columns.pop(columns.index('location'))
    columns.insert(0, location)
    df = df[columns]

    return df

if __name__ == "__main__":
    pollution_paths = [path for path in glob.glob(r'Data Collection\Data\Air Pollution\*.csv')]
    meteorological_paths = [path for path in glob.glob(r'Data Collection\Data\Meteorological\*.csv')]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        temp = [executor.submit(correlation, pollution_path, meteorological_path) for pollution_path, meteorological_path in zip(pollution_paths, meteorological_paths)]

    df = pd.DataFrame()
    for i in temp:
        df = df.append(i.result())
    
    del df['location']
    
    with open(r'Data Analysis\combined_data.csv', 'w', newline='') as f:
        f.write(df.to_csv(index=False))
