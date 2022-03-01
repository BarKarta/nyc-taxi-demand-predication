import pandas as pd

max_location = []
for i in range(12):

    print(f"Step 1 : Load NYC data month {i+1}")
    main_df = pd.read_csv(f"D:\Final Project\Data\{i+1}.csv")
    print("Step 1 Completed")

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
    main_df.rename(
        columns={
            "tpep_pickup_datetime": "pickup_datetime",
            "tpep_dropoff_datetime": "dropoff_datetime",
        },
        inplace=True,
    )
    print("Step 2 Completed")

    print("Step 3 : Loading NYC zones code Data and filtering by Manhattan")
    nyc_zones_code = pd.read_csv(r"D:\Final Project\help\taxi+_zone_lookup.csv")
    nyc_zones_code = nyc_zones_code[nyc_zones_code["Borough"] == "Manhattan"]
    list = nyc_zones_code["LocationID"].tolist()
    print("Step 3 Completed")

    print("Step 4 : Filtering the main Dataset")
    boolean_series = main_df.PULocationID.isin(list)
    manhattan_df = main_df[boolean_series].reset_index(drop=True)
    print("Step 4 Completed")

    print("Step 5 : Writing the new CSV file")
    manhattan_df.to_csv(f"D:\Final Project\Data\Manhattan_Data\{i+1}.csv", index=False)
    print(f"Step 5 Completed Month : {i+1}")
print("Finish")
print(max_location)
