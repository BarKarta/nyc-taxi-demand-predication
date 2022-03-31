import pandas as pd

# Get the Manhattan zones LocationID
nyc_zones = pd.read_csv(
    "C:\\Users\\barka\\OneDrive\\Final Project\\nyc_zones.csv")
manhattan_zones = nyc_zones.loc[nyc_zones['Borough']
                                == 'Manhattan']
manhattan_zones_ID = manhattan_zones['LocationID'].tolist()
li = []
for zone in manhattan_zones_ID:
    current_path = f'D:\\Final Project\\Data\\2019\\Manhattan_Data\\{zone}'
    df = pd.read_csv(current_path+'\\post_data_prep.csv')
    li.append(df)
main_df = pd.concat(li, axis=0, ignore_index=True)
main_df.to_csv(
    f'D:\\Final Project\\Data\\2019\\Manhattan_Data\\post_data_prep_all_zones.csv', index=False)
