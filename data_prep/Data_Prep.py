import pandas as pd
from utility import data_prep_functions as dpf
from utility.db_util import db_reader
from utility.db_util import db_writer
import sys
sys.path.append("..")


# Variables
twenty_four_hours_labels = dpf.get_hours_label(0, 24)
weather_df = dpf.get_weather_data()

for index in range(1, 13):

    print(f'Step 1: Reading The Month {index} Data')
    sql = f"""
        SELECT *
        FROM manhattan_data_{index}
        """
    main_df = db_reader(sql, 'manhattan')
    print('Step 1 Completed')

    print("Step 2: Remove duplicates and replacing the Nan's At \
          Passenger_Count to 1 ")

    main_df['pickup_datetime'] = pd.to_datetime(main_df['pickup_datetime'])
    main_df['dropoff_datetime'] = pd.to_datetime(main_df['dropoff_datetime'])
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

    print('Step 3 Completed')

    print('Step 4: Remove unnecessary Features and Outliers')
    # Drops unneccery features
    to_drop = [x for x in main_df.passenger_count if x >= 5]
    main_df = main_df[~main_df.passenger_count.isin(to_drop)]

    to_drop = [x for x in main_df.passenger_count if x <= 0]
    main_df = main_df[~main_df.passenger_count.isin(to_drop)]

    to_drop = [x for x in main_df.trip_distance if x <= 0]
    main_df = main_df[~main_df.trip_distance.isin(to_drop)]

    to_drop = [x for x in main_df.trip_time if x <= 0]
    main_df = main_df[~main_df.trip_time.isin(to_drop)]

    to_drop = [x for x in main_df.pickup_datetime.dt.year if x != 2019]
    main_df = main_df[~main_df.pickup_datetime.dt.year.isin(to_drop)]

    to_drop = [x for x in main_df.trip_time if x > 720]
    main_df = main_df[~main_df.trip_time.isin(to_drop)]

    to_drop = [x for x in main_df.speed if x <= 0]
    main_df = main_df[~main_df.speed.isin(to_drop)]

    to_drop = [x for x in main_df.pickup_date.dt.month if x != index]
    main_df = main_df[~main_df.pickup_date.dt.month.isin(to_drop)]

    # Find the Outliers for Speed, trip distance and trip time
    botrange, toprange, outliers = dpf.get_outliers(main_df, main_df['speed'])
    to_drop = [x for x in main_df.speed if x > toprange or x < botrange]
    main_no_outliers_df = main_df[~main_df.speed.isin(to_drop)]
    botrange, toprange, outliers = dpf.get_outliers(
        main_df, main_df['trip_distance'])
    to_drop = [x for x in main_df.trip_distance if x >
               toprange or x < botrange]
    main_no_outliers_df = main_df[~main_df.trip_distance.isin(to_drop)]
    botrange, toprange, outliers = dpf.get_outliers(
        main_df, main_df['trip_time'])
    to_drop = [x for x in main_df.trip_time if x > toprange or x < botrange]
    main_no_outliers_df = main_df[~main_df.trip_time.isin(to_drop)]
    main_no_outliers_df.reset_index(inplace=True, drop=True)
    main_df = main_no_outliers_df
    print('Step 4 Completed')

    print('Step 5: Merge with Weather Data')
    weather_df['pickup_date'] = pd.to_datetime(
        weather_df["pickup_date"].dt.strftime('%Y-%m-%d'))
    main_df['pickup_date'] = pd.to_datetime(
        main_df["pickup_date"].dt.strftime('%Y-%m-%d'))
    main_df.sort_values('pickup_date', inplace=True)
    main_df = pd.merge_asof(main_df, weather_df, on='pickup_date')
    print('Step 5: Completed')

    print('Step 6: Removing unnecessary features and fixing Weather Data')
    main_df.drop(['pickup_datetime'], axis=1, inplace=True)
    main_df.drop(['pickup_time'], axis=1, inplace=True)

    main_df['Precipitation'].replace('T', '0.00001', inplace=True)
    main_df['New Snow'].replace('T', '0.00001', inplace=True)
    main_df['Snow Depth'].replace('T', '0.00001', inplace=True)

    main_df['Precipitation'] = main_df['Precipitation'].astype(float)
    main_df['New Snow'] = main_df['New Snow'].astype(float)
    main_df['Snow Depth'] = main_df['Snow Depth'].astype(float)
    print('Step 6 Completed')

    print('Step 7: Groupby')
    main_df = main_df.groupby(
        ['PULocationID', 'pickup_date', 'time_binned']
    ).agg({
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
                            'New Snow': 'new_snow', 'Snow Depth': 'snow_depth',
                            'PULocationID': 'zone'},
                   inplace=True)
    main_df = main_df[['zone', 'pickup_date', 'weekday', 'time_binned', 'Tmax',
                       'Tmin',
                       'Tavg', 'Tdep', 'HDD', 'CDD', 'Precipitation',
                       'new_snow', 'snow_depth', 'trip_distance', 'trip_time',
                       'speed', 'num_of_taxis']]
    print('Step 7 Completed')

    print('Step 8: Write to DB')
    db_writer(main_df, f'Data_{index}', 'post_prep')
    print('Step 8 Completed')

print('Finish')
