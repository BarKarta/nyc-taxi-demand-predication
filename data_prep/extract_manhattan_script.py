""" The script extracts the manhattan data from the all the nyc data.
    it also drops unnecessary features.
    """
from typing import Final
import pandas as pd
from utility import data_prep_functions as dpf
import os

# CONST
NYC_DATA_PATH: Final = r'D: \Final Project\Data'
OUTPUT_PATH: Final = r'D:\Final Project\Data\Manhattan_Data'
for i in range(12):

    # Loads the NYC data
    print(f"Step 1 : Load NYC data month {i+1}")
    main_df = pd.read_csv(os.join(NYC_DATA_PATH, f'{i+1}.csv'))
    print("Step 1 Completed")

    # Drops Unnecessary features
    print("Step 2 : Dropping Features and Renaming")
    main_df.drop(
        [
            "VendorID",
            "RatecodeID",
            "store_and_fwd_flag",
            "payment_type",
            "fare_amount",
            "extra",
            "mta_tax",
            "tip_amount",
            "tolls_amount",
            "improvement_surcharge",
            "total_amount",
            "congestion_surcharge",
        ],
        axis=1,
        inplace=True,
    )

    # Renames some features for easier understanding
    main_df.rename(
        columns={
            "tpep_pickup_datetime": "pickup_datetime",
            "tpep_dropoff_datetime": "dropoff_datetime",
        },
        inplace=True,
    )
    print("Step 2 Completed")

    # Filters the data by using a list of manhattan ID's
    print("Step 3 : Filtering the main Dataset")
    list = dpf.get_manhattan_zones_ID
    boolean_series = main_df.PULocationID.isin(list)
    manhattan_df = main_df[boolean_series].reset_index(drop=True)
    print("Step 3Completed")

    # Writes the data to a different folder
    print("Step 5 : Writing the new CSV file")
    manhattan_df.to_csv(os.join(OUTPUT_PATH, f'{i+1}.csv'), index=False)
    print(f"Step 5 Completed Month : {i+1}")

print("Finish")
