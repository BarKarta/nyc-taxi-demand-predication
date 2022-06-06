"""The Script Takes each ZONE and run the proccess of data preperation on it.
    After each the proccess of each zone it saves it to a new csv file
    """
import pandas as pd
import os
import glob

from utility import data_prep_functions as dpf
from typing import Final


# CONST
MANHATTAN_DATA_PATH: Final[str] = r"D: \Final Project\Data\2019\Manhattan_Data"

# Variables
twenty_four_hours_labels = dpf.get_hours_label(0, 24)
li = []  # Temp List which will contain the df to contact


# Get the Manhattan zones LocationID
manhattan_zones_ID = dpf.get_manhattan_zones_ID()

# Weather Data
weather_df = dpf.get_weather_data()

# Loops through all the Zones
for zone in manhattan_zones_ID:

    print(f"Zone # {zone}")
    print("Step 1: Concating all the months")
    # zones dir
    zone_path = os.join(MANHATTAN_DATA_PATH, zone)

    # Gets all the files and concat them
    all_files = glob.glob(os.join(zone_path, '*.csv'))
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)
    main_df = pd.concat(li, axis=0, ignore_index=True)

    print("Step 1 Completed")

    # Remove Duplicates & replacing the Nan's At Passenger_Count to 1
    print("Step 2: Remove duplicates and replacing the Nan's At \
          Passenger_Count to 1 ")
    print(main_df.duplicated().sum())  # Prints the number of duplicates
    main_df.drop_duplicates(inplace=True)  # Removing Duplicates
    main_df['passenger_count'] = main_df['passenger_count'].fillna(1)
    main_df.dropna(inplace=True)  # Drops rows with Nan values

    print("Step 2 Completed")

    print("Step 3: Changing features")
    # Converting the Date columns to DateTime type.
    main_df['pickup_datetime'] = pd.to_datetime(main_df['pickup_datetime'])
    main_df['dropoff_datetime'] = pd.to_datetime(main_df['dropoff_datetime'])
    # Getting the delta between the pick up and drop off in a new column.
    main_df['trip_time'] = dpf.time_delta(
        main_df['pickup_datetime'], main_df['dropoff_datetime'])

    # Creating a speed column
    main_df['speed'] = (main_df.trip_distance / (main_df.trip_time / 60))

    # Creating a PU date and time
    main_df['pickup_date'] = pd.to_datetime(main_df['pickup_datetime']).dt.date
    main_df['pickup_time'] = pd.to_datetime(main_df['pickup_datetime']).dt.time
    main_df['pickup_date'] = pd.to_datetime(main_df['pickup_date'])

    # Creating Time Bins
    bins = [x for x in range(25)]
    main_df['time_binned'] = pd.cut(
        main_df.pickup_datetime.dt.hour, bins, labels=twenty_four_hours_labels,
        right=False)

    # Drops unneccery features
    main_df.drop(['dropoff_datetime', 'PULocationID',
                 'DOLocationID'], axis=1, inplace=True)
    print("Step 3 Completed")

    # Drops Junk Data
    print("Step 4: Data Cleaning")
    main_df.drop(main_df[main_df['passenger_count'] >= 5].index,
                 axis=0, inplace=True)  # num of passengers > 5
    main_df.drop(main_df[main_df['passenger_count'] <= 0].index,
                 axis=0, inplace=True)  # num of passengers < 0
    main_df.drop(main_df[main_df['trip_distance'] <= 0].index,
                 axis=0, inplace=True)  # trip distance < 0
    main_df.drop(main_df[main_df['trip_time'] <= 0].index,
                 axis=0, inplace=True)  # trip time <= 0
    main_df.drop(main_df[main_df['pickup_datetime'].dt.year !=
                 2019].index, axis=0, inplace=True)  # dates not from 2019
    main_df.drop(main_df[main_df['trip_time'] > 720].index,
                 axis=0, inplace=True)  # time > 12 hours
    main_df.drop(main_df[main_df['speed'] <= 0].index,
                 axis=0, inplace=True)  # speed <= 0

    # Find the Outliers for Speed, trip distance and trip time
    botrange, toprange, outliers = dpf.get_outliers(main_df, main_df['speed'])
    index_list = [i for i in main_df.index if i not in outliers.index]
    main_no_outliers_df = main_df.loc[index_list]
    botrange, toprange, outliers = dpf.get_outliers(
        main_df, main_df['trip_distance'])
    index_list = [
        i for i in main_no_outliers_df.index if i not in outliers.index]
    main_no_outliers_df = main_no_outliers_df.loc[index_list]
    botrange, toprange, outliers = dpf.get_outliers(main_df,
                                                    main_df['trip_time'])
    index_list = [
        i for i in main_no_outliers_df.index if i not in outliers.index]
    main_no_outliers_df = main_no_outliers_df.loc[index_list]
    main_no_outliers_df.reset_index(inplace=True, drop=True)
    main_df = main_no_outliers_df

    # Merge the weather Data with the main data
    weather_df['pickup_date'] = pd.to_datetime(
        weather_df["pickup_date"].dt.strftime('%Y-%m-%d'))
    main_df['pickup_date'] = pd.to_datetime(
        main_df["pickup_date"].dt.strftime('%Y-%m-%d'))
    main_df.sort_values('pickup_date', inplace=True)
    main_df = pd.merge_asof(main_df, weather_df, on='pickup_date')

    # Drops more unneeded features and also , tackling some data problems with
    # the weather data
    main_df.drop(['pickup_datetime'], axis=1, inplace=True)
    main_df.drop(['pickup_time'], axis=1, inplace=True)

    main_df['Precipitation'].replace('T', '0.00001', inplace=True)
    main_df['New Snow'].replace('T', '0.00001', inplace=True)
    main_df['Snow Depth'].replace('T', '0.00001', inplace=True)

    main_df['Precipitation'] = main_df['Precipitation'].astype(float)
    main_df['New Snow'] = main_df['New Snow'].astype(float)
    main_df['Snow Depth'] = main_df['Snow Depth'].astype(float)

    # Changing for easier stats test
    main_df = main_df.groupby(['pickup_date', 'time_binned']).agg({
        'Tmax': 'mean',
        'Tmin': 'mean',
        'Tavg': 'mean',
        'Tdep': 'mean',
        'HDD': 'mean',
        'CDD': 'mean',
        'Precipitation': 'mean',
        'New Snow': 'mean',
        'Snow Depth': 'mean',
        'trip_distance': 'mean',
        'trip_time': 'mean',
        'speed': 'mean',
        'passenger_count': 'count',
    }).reset_index()
    main_df['weekday'] = main_df['pickup_date'].dt.day_name()
    main_df.rename(columns={'passenger_count': 'num_of_taxis',
                   'New Snow': 'new_snow', 'Snow Depth': 'snow_depth'},
                   inplace=True)
    main_df = main_df[['pickup_date', 'weekday', 'time_binned', 'Tmax', 'Tmin',
                       'Tavg', 'Tdep', 'HDD', 'CDD', 'Precipitation',
                       'new_snow', 'snow_depth', 'trip_distance', 'trip_time',
                       'speed', 'num_of_taxis']]

    # Adds a Zone colum
    main_df['Zone'] = zone

    # Save the new Dataframe to a CSV
    main_df.to_csv(
        f'D:\\Final Project\\Data\\2019\\Manhattan_Data\\{zone}\
            \\post_data_prep.csv',
        index=False)
print('Finish')
