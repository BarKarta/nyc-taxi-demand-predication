import pandas as pd
import glob

from pip import main


def write_to_Log(x):
    """Function writes to a log file."""
    with open(r'D:\Final Project\Data\2019\Manhattan_Data\log_file.text', 'a') as file:
        file.write(x)


def get_outliers(df, series):
    """Returns Outliers"""
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    if q1*q3 == 0:
        iqr = abs(2*(q1+q3))
        toprange = iqr
        botrange = -toprange
    else:
        iqr = q3-q1
        toprange = q3 + iqr * 1.5
        botrange = q1 - iqr * 1.5

    outliers_top = df[series > toprange]
    outliers_bot = df[series < botrange]
    outliers = pd.concat([outliers_bot, outliers_top], axis=0)

    return (botrange, toprange, outliers)


# Variables
twenty_four_hours_labels = labels = ['00:00 - 00:59',
                                     '01:00 - 01:59',
                                     '02:00 - 02:59',
                                     '03:00 - 03:59',
                                     '04:00 - 04:59',
                                     '05:00 - 05:59',
                                     '06:00 - 06:59',
                                     '07:00 - 07:59',
                                     '08:00 - 08:59',
                                     '09:00 - 09:59',
                                     '10:00 - 10:59',
                                     '11:00 - 11:59',
                                     '12:00 - 12:59',
                                     '13:00 - 13:59',
                                     '14:00 - 14:59',
                                     '15:00 - 15:59',
                                     '16:00 - 16:59',
                                     '17:00 - 17:59',
                                     '18:00 - 18:59',
                                     '19:00 - 19:59',
                                     '20:00 - 20:59',
                                     '21:00 - 21:59',
                                     '22:00 - 22:59',
                                     '23:00 - 23:59'
                                     ]  # A 24H labels


# Get the Manhattan zones LocationID
nyc_zones = pd.read_csv(
    "C:\\Users\\barka\\OneDrive\\Final Project\\nyc_zones.csv")
manhattan_zones = nyc_zones.loc[nyc_zones['Borough']
                                == 'Manhattan']
manhattan_zones_ID = manhattan_zones['LocationID'].tolist()

# Weather Data
weather_df = pd.read_csv(
    'C:\\Users\\barka\\OneDrive\\Final Project\\Data\\NYC Weather.csv')
weather_df['Date'] = pd.to_datetime(weather_df['Date'], format='%d/%m/%Y')
weather_df.rename(columns={'Date': 'pickup_date'}, inplace=True)

for zone in manhattan_zones_ID:

    print(f"Zone # {zone}")
    print("Step 1: Concating all the months")
    # zones dir
    zone_path = f"D:\\Final Project\\Data\\2019\\Manhattan_Data\\{zone}"
    li = []
    # Gets all the files and concat them
    all_files = glob.glob(zone_path + "/*.csv")
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)
    main_df = pd.concat(li, axis=0, ignore_index=True)
    print("Step 1 Completed")

    write_to_Log(f'Zone {zone}\n')
    write_to_Log(f'Zone Length {len(main_df)}\n')

    # Remove Duplicates & replacing the Nan's At Passenger_Count to 1
    print("Step 2: Remove duplicates and replacing the Nan's At Passenger_Count to 1 ")
    print(main_df.duplicated().sum())  # Prints the number of duplicates
    main_df.drop_duplicates(inplace=True)  # Removing Duplicates
    main_df['passenger_count'] = main_df['passenger_count'].fillna(1)
    # If we have a lot of missing values we write it to a log file.
    if main_df.isnull().sum().sum() >= (len(main_df)/100)*10:
        write_to_Log(
            f'Zone has more than 10% missing information NEED to be Fixed Manually\n')
    else:
        main_df.dropna(inplace=True)
    print("Step 2 Completed")

    print("Step 3: Changing features")
    # Converting the Date columns to DateTime type.
    main_df['pickup_datetime'] = pd.to_datetime(main_df['pickup_datetime'])
    main_df['dropoff_datetime'] = pd.to_datetime(main_df['dropoff_datetime'])
    # Getting the delta between the pick up and drop off in a new column.
    t1 = main_df['pickup_datetime']
    t2 = main_df['dropoff_datetime']
    # Adding a Trip_time column based.
    main_df['trip_time'] = (t2-t1).dt.total_seconds()/60
    # Creating a speed column
    main_df['speed'] = (main_df.trip_distance / (main_df.trip_time / 60))
    # Creating a PU date and time
    main_df['pickup_date'] = pd.to_datetime(main_df['pickup_datetime']).dt.date
    main_df['pickup_time'] = pd.to_datetime(main_df['pickup_datetime']).dt.time
    main_df['pickup_date'] = pd.to_datetime(main_df['pickup_date'])
    # Creating Time Bins
    bins = [x for x in range(25)]
    main_df['time_binned'] = pd.cut(
        main_df.pickup_datetime.dt.hour, bins, labels=twenty_four_hours_labels, right=False)
    # Drops unneccery features
    main_df.drop(['dropoff_datetime', 'PULocationID',
                 'DOLocationID'], axis=1, inplace=True)
    print("Step 3 Completed")

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

    # Find the Outliers for Speed
    botrange, toprange, outliers = get_outliers(main_df, main_df['speed'])
    index_list = [i for i in main_df.index if i not in outliers.index]
    main_no_outliers_df = main_df.loc[index_list]
    botrange, toprange, outliers = get_outliers(
        main_df, main_df['trip_distance'])
    index_list = [
        i for i in main_no_outliers_df.index if i not in outliers.index]
    main_no_outliers_df = main_no_outliers_df.loc[index_list]
    botrange, toprange, outliers = get_outliers(main_df, main_df['trip_time'])
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

    # Drops more unneeded features and also , tackling some data problems with the weather data
    main_df.drop(['pickup_datetime'], axis=1, inplace=True)
    main_df.drop(['pickup_time'], axis=1, inplace=True)

    main_df['Precipitation'].replace('T', '0.00001', inplace=True)
    main_df['New Snow'].replace('T', '0.00001', inplace=True)
    main_df['Snow Depth'].replace('T', '0.00001', inplace=True)

    main_df['Precipitation'] = main_df['Precipitation'].astype(float)
    main_df['New Snow'] = main_df['New Snow'].astype(float)
    main_df['Snow Depth'] = main_df['Snow Depth'].astype(float)

    # Changing the dataframe to fit our algo
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
                   'New Snow': 'new_snow', 'Snow Depth': 'snow_depth'}, inplace=True)
    main_df = main_df[['pickup_date', 'weekday', 'time_binned', 'Tmax', 'Tmin', 'Tavg', 'Tdep', 'HDD', 'CDD', 'Precipitation', 'new_snow', 'snow_depth', 'trip_distance', 'trip_time',
                       'speed', 'num_of_taxis']]

    # Adds a Zone colum
    main_df['Zone'] = zone

    # Save the new Dataframe to a CSV
    main_df.to_csv(
        f'D:\\Final Project\\Data\\2019\\Manhattan_Data\\{zone}\\post_data_prep.csv', index=False)
    write_to_Log('\n')
print('Finish')
