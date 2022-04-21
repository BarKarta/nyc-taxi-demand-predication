"""This script is taking all the post prep data that is seperated to 12 months
    and combine them into a single file.
    So we can work on a single DF.
"""

from typing import Final
import pandas as pd
import os

# CONST
NYC_ZONES_CSV_PATH: Final[str] = r"C:\Users\barka\OneDrive\Final Project\nyc_zones.csv"
DATA_PATH: Final[str] = r"D: \Final Project\Data\2019\Manhattan_Data"
# Load the NYC zones ID.
nyc_zones = pd.read_csv(NYC_ZONES_CSV_PATH)

# Manhattan_zones is a DF which contains only the data about Manhattan zones.
manhattan_zones = nyc_zones.loc[nyc_zones['Borough']
                                == 'Manhattan']

# Get the list of the ID's.
manhattan_zones_ID = manhattan_zones['LocationID'].tolist()
li = []
# Loops through each zone ( Each Zone has it folder with the post prep data)
for zone in manhattan_zones_ID:
    current_path = os.join(DATA_PATH, zone)  # Set the path to each zone
    df = pd.read_csv(os.join(current_path, 'post_data_prep.csv'))
    li.append(df)  # Adds the df to the list
# Concat all the df's to one
main_df = pd.concat(li, axis=0, ignore_index=True)
# Saves the df to the output location
main_df.to_csv(
    os.join(DATA_PATH, 'post_data_prep_all_zones.csv'), index=False)
