
from typing import Tuple, List, Final
import pandas as pd

# CONST
post_data_prep_all_zone_PATH: Final = r'C:\Users\barka\OneDrive'\
    r'\Final Project\Data\Manhattan\2019\post_data_prep_all_zones.csv'


def load_post_data_prep_all_zone() -> pd.DataFrame:
    """ Loads the csv which includes the post data with all the zones.

    Returns:
        DataFrame: returns the currect dataframe.
    """
    return pd.read_csv(post_data_prep_all_zone_PATH)


def get_dummies(cat_features: list, df: pd.DataFrame) -> pd.DataFrame:
    """ Converts the catergorial features to a numeric features

    Args:
        cat_features (list): List of the catergorial features in the dataframe
                             that yo want to turn into numeric features
        df (pd.DataFrame): The DataFrame which u want to convert
                            the catergorial features to numeric features

    Returns:
        pd.DataFrame: dateframe with converted features
    """
    for feature in cat_features:
        temp_dummy = pd.get_dummies(df[feature])
        df = pd.merge(left=temp_dummy, right=df,
                      left_index=True, right_index=True)
    df = df.drop(cat_features, axis=1)
    return df


def swap_first_and_last_col(df: pd.DataFrame) -> pd.DataFrame:
    """swaps the columns location in the Datframe, replace between the first
         and last

    Args:
        df (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    cols = df.columns.to_list()
    df = df[cols[-1:] + cols[:-1]]
    return df


def split_X_y(df: pd.DataFrame, target_feature: str) -> Tuple[List[str], pd.DataFrame]:
    """ split the data into two, dataframe with out the target feature,
        and an array of the target feature.

    Args:
        df (pd.DataFrame): Dataframe
        target_feature (_type_): the target feature you want to train your
                                 model for

    Returns:
        List, pd.pd.DataFrame: y,X
    """
    y = df[target_feature]
    temp = df.drop(target_feature, axis=1)
    X = temp
    return y, X
