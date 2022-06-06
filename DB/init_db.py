from utility import db_util
import os
import pandas as pd
from typing import Final
import sys
sys.path.append("..")


# Constants
RAW_DATA_PATH = r'../Raw_data'

# Writes Raw NYC taxi data
for i in range(12):
    print(f'Reading File {i+1}')
    file_name = f'{i+1}.csv'
    file_path = os.path.join(RAW_DATA_PATH, file_name)
    df = pd.read_csv(file_path)
    print(f'Writing File {i+1} to Db')
    db_util.db_writer(df, f'month_{i+1}', 'nyc_taxis_db')
    print(f'Done File {i+1}')
print('Finish')

# Writes Weather Data
weather_file_name = 'nyc_weather.csv'
weather_file_name = os.path.join(RAW_DATA_PATH, weather_file_name)
weather_df = pd.read_csv(weather_file_name)
db_util.db_writer(weather_df, 'weather_data', 'nyc_taxis_db')

# Writes Zones Data
nyc_zones_name = 'nyc_zones.csv'
nyc_zones_path = os.path.join(RAW_DATA_PATH, nyc_zones_name)
zones_df = pd.read_csv(nyc_zones_path)
db_util.db_writer(zones_df, 'nyc_zones', 'nyc_taxis_db')
