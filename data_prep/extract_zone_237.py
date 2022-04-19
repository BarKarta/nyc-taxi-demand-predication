import pandas as pd

max_location = []
for i in range(12):

    print(f"Step 1 : Load NYC data month {i+1}")
    manhattan_df = pd.read_csv(f"D:\Final Project\Data\Manhattan_Data\{i+1}.csv")
    print("Step 1 Completed")

    print("Step : 2 Extract Zone 273")
    zone_237 = manhattan_df.loc[manhattan_df["PULocationID"] == 237]
    print("Step 2 Completed")

    print("Step 3 : Writing the new CSV file")
    zone_237.to_csv(
        f"D:\Final Project\Data\Manhattan_Data\zone_237\{i+1}.csv", index=False
    )
    print(f"Step 3 Completed Month : {i+1}")

print("Finish")
