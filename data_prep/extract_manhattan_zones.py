""" The scripts takes the manhattan data which was extract out of all the data
    and separate it into zones, each zones gets 12 csv represending each month.
"""

from typing import Final
import pandas as pd
import os as os
from utility import data_prep_functions as dpf

# CONST
MANHATTAN_DATA_PATH: Final[str] = r"C:\Users\barka\OneDrive\Final Project\
    \nyc_zones.csv"
PARENT_DIR: Final[str] = r"D:\Final Project\Data\2019\Manhattan_Data"
MODE: Final = 0o666

# Gets Manhattan zones ID
manhattan_zones_ID = dpf.get_manhattan_zones_ID()

# For each Month Data, it creates a zone folder if not exists and then in that
# folder it create the a csv with that month.
for i in range(12):
    print(f"Step 1 : Load NYC data month {i+1}")
    manhattan_df = pd.read_csv(
        f"D:\\Final Project\\Data\\2019\\Manhattan_Data\\Months\\{i+1}.csv")
    print("Step 1 Completed")

    # for each zone creates a csv in the current month the loop is.
    for zone in manhattan_zones_ID:

        print(f"Step : 2 Extract Zone {zone}")
        current_zone = manhattan_df.loc[manhattan_df["PULocationID"] == zone]
        print("Step 2 Completed")

        current_path = os.path.join(PARENT_DIR, str(zone))
        if not os.path.isdir(current_path):  # Checks if folder exists
            os.mkdir(current_path, MODE)
            print(f'Folder Created {current_path}')

        print("Step 3 : Writing the new CSV file")
        current_zone.to_csv(
            f"D: \\Final Project\\Data\\2019\\Manhattan_Data\
            {zone}\\{i+1}.csv",
            index=False
        )  # Creates the csv
    print(f"Step 3 Completed Month : {i+1}")

print("Finish")
