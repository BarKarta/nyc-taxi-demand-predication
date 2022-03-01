import pandas as pd

max_location = []
for i in range(12):
    print(f"Step 1 : Load NYC data month {i+1}")
    manhattan_df = pd.read_csv(f"D:\Final Project\Data\Manhattan_Data\{i+1}.csv")
    print("Step 1 Completed")
    print("Step 2 : Find the locationID with max Value")
    manhattan_df_zones = manhattan_df.groupby("PULocationID", as_index=False).count()
    max_index = manhattan_df_zones["passenger_count"].idxmax()
    max_location.append(
        (manhattan_df_zones.loc[manhattan_df_zones.index == max_index]).iloc[0][
            "PULocationID"
        ]
    )
    print("Step 2 Completed")

print(max_location)
