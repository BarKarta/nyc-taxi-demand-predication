""" The script extracts the manhattan data from all the nyc data.
    it also drops unnecessary features.
    """
from utility.db_util import db_reader
from utility.db_util import db_writer
from utility import data_prep_functions as dpf
import sys
sys.path.append("..")


<<<<<<< HEAD
=======
# CONST
NYC_DATA_PATH: Final[str] = r'D: \Final Project\Data'
OUTPUT_PATH: Final[str] = r'D:\Final Project\Data\Manhattan_Data'
>>>>>>> 46a0ad1752917e44cfc7d59eef06c25e201b7ce4
for i in range(12):

    # Loads the NYC data
    print(f"Step 1 : Load NYC data month {i}")
    sql = f"""
            SELECT *
            FROM month_{i}
            """
    main_df = db_reader(sql, 'nyc_taxis_db')
    print("Step 1 Completed")

    # Drops Unnecessary features
    print("Step 2 : Dropping Features and Renaming")
    main_df.drop(
        [
            "index",
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
    list = dpf.get_manhattan_zones_ID()
    boolean_series = main_df.PULocationID.isin(list)
    manhattan_df = main_df[boolean_series].reset_index(drop=True)
    print("Step 3 Completed")

    # Writes the data to a different folder
    print("Step 5 : Writing the new CSV file")
    db_writer(manhattan_df, f'manhattan_data_{i+1}', 'manhattan')
    print(f"Step 5 Completed Month : {i+1}")

print("Finish")
