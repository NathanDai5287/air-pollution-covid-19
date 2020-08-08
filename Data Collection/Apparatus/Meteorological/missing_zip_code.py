import glob

zip_codes = [zip_code[-8:-4] for zip_code in glob.glob(r'Data Collection\Data\Meteorological\*.csv')]

with open(r'Data Collection\Apparatus\Docs\zip_codes.csv') as f:
    target = [zip_code.strip(',\n') for zip_code in f.readlines()][:3000]
print(list(set(zip_codes + target)))

with open('code.csv', 'w') as f:
    for code in zip_codes:
        f.write(code.zfill(5) + ',\n')
