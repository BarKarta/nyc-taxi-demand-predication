import numpy as np
from utility.db_util import db_reader
from utility.db_util import db_writer
import pandas as pd
import sys
sys.path.append("..")


li = []
for i in range(12):
    sql = f"""
            SELECT *
            FROM Data_{i+1}
            """
    df = db_reader(sql, 'post_prep')
    li.append(df)
main_df = pd.concat(li, axis=0, ignore_index=True)

main_df.dropna(inplace=True)
main_df.drop_duplicates(inplace=True)
main_df.drop(['pickup_date', 'trip_distance', 'speed'], axis=1, inplace=True)
main_df['trip_time'] = main_df.trip_time.apply(np.ceil)

under_11min_ride_df = main_df.loc[main_df.trip_time <= 10].copy()
between_11min_and_13min_ride_df = main_df.loc[(
    main_df.trip_time >= 11) & (main_df.trip_time < 14)].copy()
between_14min_and_25_min_ride_df = main_df.loc[(
    main_df.trip_time >= 14) & (main_df.trip_time <= 25)].copy()

db_writer(under_11min_ride_df, 'under_11min_ride_df', 'post_procces_data')
db_writer(between_11min_and_13min_ride_df,
          'between_11min_and_13min_ride_df', 'post_procces_data')
db_writer(between_14min_and_25_min_ride_df,
          'between_14min_and_25_min_ride_df', 'post_procces_data')
db_writer(main_df, 'data_combined', 'post_procces_data')
