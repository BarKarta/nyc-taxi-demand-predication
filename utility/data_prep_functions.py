""" This Module contains functions which used in the data preperation proccess.
    """

from typing import Final, List
import pandas as pd

# CONST
MANHATTAN_ZONES_PATH: Final = r"C:\Users\barka\OneDrive\Final Project\nyc_zones.csv"
WEATHER_CSV_PATH = r'C:\Users\barka\OneDrive\Final Project\Data\NYC Weather.csv'


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


def get_hours_label(min: int, max: int) -> List:
    """ the function creates a list of labels in the format 00:00 - 00:59 for
        example

    Args:
        min (int): min hour (0)
        max (int): max hour (24)

    Returns:
        List: Returns a list of strings ( labels )
    """
    return [f'{s:02d} - {s:02d}' for s in range(min, max)]


def get_manhattan_zones_ID() -> List:
    """ Returns the manhattan zones ID so  we can use it to filter later

    Returns:
        List: List of ID's
    """
    nyc_zones = pd.read_csv(MANHATTAN_ZONES_PATH)
    manhattan_zones = nyc_zones.loc[nyc_zones['Borough']
                                    == 'Manhattan']
    manhattan_zones_ID = manhattan_zones['LocationID'].tolist()
    return manhattan_zones_ID


def get_weather_data() -> pd.DataFrame:
    """ Returns the Weather CSV as a Datframe

    Returns:
        pd.DataFrame: Contains the Weather Data
    """
    weather_df = pd.read_csv(WEATHER_CSV_PATH)
    weather_df['Date'] = pd.to_datetime(weather_df['Date'], format='%d/%m/%Y')
    weather_df.rename(columns={'Date': 'pickup_date'}, inplace=True)
    return weather_df


def time_delta(time1: pd.Series, time2: pd.Series) -> pd.Series:
    return (time2-time1).dt.total_seconds()/60
