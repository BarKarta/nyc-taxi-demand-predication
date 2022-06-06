import os
import pickle
from typing import Final, List
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import warnings
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
import utility.utility_functions as ut
import sys
sys.path.append("..")

warnings.simplefilter(action='ignore', category=FutureWarning)

MODEL_NAME: Final[str] = 'ML_model.sav'


def get_rmse_for_df(df_input: pd.DataFrame, df_name: str) -> int:

    df = df_input.copy()
    df.dropna(inplace=True)
    df.reset_index(inplace=True, drop=True)

    main_df = ut.get_dummies(['weekday', 'time_binned', 'Season'], df)
    main_df = ut.swap_first_and_last_col(main_df)
    y, X = ut.split_X_y(main_df, 'num_of_taxis')

    scaler = MinMaxScaler()
    scaled_X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

    # features = main_df.columns.tolist()
    model_lr = LinearRegression()
    model_lr.fit(X, y)
    importance = model_lr.coef_

    feature_dict = {'Features': X.columns.tolist(), 'Score': importance}
    feature_importance_sorted = pd.DataFrame(feature_dict).sort_values(
        by=['Score'], ascending=True)['Features']

    X_train_scaled, X_test_scaled, y_train, y_test = train_test_split(
        scaled_X, y, test_size=0.3, random_state=123)

    # Backwards
    X_train_scaled_backwards = X_train_scaled.copy()
    backward_rmse_list = []
    backward_best_rmse = np.std(y)
    for feature in (feature_importance_sorted):
        xg_reg = xgb.XGBRegressor(objective='reg:squarederror',
                                  colsample_bytree=0.3, learning_rate=0.1,
                                  max_depth=5, alpha=10, n_estimators=10)
        xg_reg.fit(X_train_scaled_backwards, y_train)
        train_pred = xg_reg.predict(X_train_scaled_backwards)
        rmse_train = np.sqrt(mean_squared_error(y_train, train_pred))
        backward_rmse_list.append(rmse_train)
        if backward_best_rmse > rmse_train:
            backward_best_rmse = rmse_train
            backward_best_model = xg_reg
            backward_best_features = X_train_scaled_backwards.columns.tolist()

        X_train_scaled_backwards.drop(feature, axis=1, inplace=True)

    # Forwards
    forward_rmse_list = []
    forward_best_rmse = np.std(y)
    forward_list = []
    X_train_scaled_forward = []
    for feature in list(reversed(feature_importance_sorted.tolist())):
        forward_list.append(feature)
        X_train_scaled_forward = X_train_scaled[forward_list]
        xg_reg = xgb.XGBRegressor(objective='reg:squarederror',
                                  colsample_bytree=0.3, learning_rate=0.1,
                                  max_depth=5, alpha=10, n_estimators=10)
        xg_reg.fit(X_train_scaled_forward, y_train)
        train_pred = xg_reg.predict(X_train_scaled_forward)
        rmse_train = np.sqrt(mean_squared_error(y_train, train_pred))
        forward_rmse_list.append(rmse_train)
        if forward_best_rmse > rmse_train:
            forward_best_model = xg_reg
            forward_best_rmse = rmse_train
            forward_best_features = X_train_scaled_forward.columns.tolist()

    # Checks what is better
    if forward_best_rmse > backward_best_rmse:
        test_rmse = getTestResult(
            backward_best_model, X_test_scaled, y_test, backward_best_features)
        saveData(backward_best_model, backward_best_features, df_name)
        return backward_best_rmse, np.std(y), test_rmse
    else:
        test_rmse = getTestResult(
            forward_best_model, X_test_scaled, y_test, forward_best_features)
        saveData(forward_best_model, forward_best_features, df_name)
        return forward_best_rmse, np.std(y), test_rmse


def saveData(model, features: List[str], df_name: str):
    NEW_PATH: Final[str] = r'..\models_data'
    folder_path = os.path.join(NEW_PATH, df_name)
    os.mkdir(folder_path)

    # Saves the features
    with open(f'..\\models_data\\{df_name}\\best_features.txt',
              'w') as file:
        for feature in features:
            file.write("%s\n" % feature)
    # Saves the best Model
    with open(f'..\\models_data\\{df_name}\\best_model.sav', 'wb') as f:
        pickle.dump(model, f)


def getTestResult(model, x_test, y_test, features) -> int:
    x_test = x_test[features]
    pred = model.predict(x_test)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    return rmse
