from genericpath import isdir
import pandas as pd
import os as os

max_location = []
nyc_zones = pd.read_csv(
    "C:\\Users\\barka\\OneDrive\\Final Project\\nyc_zones.csv")
manhattan_zones = nyc_zones.loc[nyc_zones['Borough']
                                == 'Manhattan']
manhattan_zones_ID = manhattan_zones['LocationID'].tolist()
parent_dir = "D:\\Final Project\\Data\\2019\\Manhattan_Data"
mode = 0o666
for i in range(12):
    print(f"Step 1 : Load NYC data month {i+1}")
    manhattan_df = pd.read_csv(
        f"D:\\Final Project\\Data\\2019\\Manhattan_Data\\Months\\{i+1}.csv")
    print("Step 1 Completed")
    for zone in manhattan_zones_ID:
        print(f"Step : 2 Extract Zone {zone}")
        current_zone = manhattan_df.loc[manhattan_df["PULocationID"] == zone]
        print("Step 2 Completed")
        current_path = os.path.join(parent_dir, str(zone))
        if not os.path.isdir(current_path):
            os.mkdir(current_path, mode)
            print(f'Folder Created {current_path}')
        print("Step 3 : Writing the new CSV file")
        current_zone.to_csv(
            f"D:\\Final Project\\Data\\2019\\Manhattan_Data\\{zone}\\{i+1}.csv", index=False
        )
    print(f"Step 3 Completed Month : {i+1}")
print("Finish")
