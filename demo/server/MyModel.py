""" MyModel class is responsable for the the Machine Learning models.
    Loads the currect model based on the input and choose the correct
    features for each model based on the data which is stored at Models_data
    folder.
"""
import pickle
from typing import Final, List
import os
import pandas as pd
from datetime import datetime
import sys


class MyModel:
    def __init__(self, features: dict, time: str, date: str) -> None:
        """ Constructor set the features as a dict and the time and date.
        Args:
            features (dict): a dict of features for the model, it contains all
                                the features that each model might use.
            time (str): Time, is the input time from the user, the class is
                                using it to get the correct model.
            date (str): Date, is the input date from the user, the class is
                                using it to get the correct model.
        """
        self.date = date
        self.time = time
        self.features = features
        self.chosen_model = self.__chooseModel()
        model_path = self.chosen_model.path
        with open(os.path.join(model_path, 'best_model.sav'), 'rb') as f:
            self.loaded_model = pickle.load(f)  # Loads the Model

    def runModel(self):
        """ A public functions which runs the model and returns the
            array which include the prediction.
        Returns:
            Array: Prediction
        """
        input_df = self.__createDF()  # Creates a Datefrom from the input
        prediction = self.loaded_model.predict(input_df)
        return prediction

    def __createDF(self):
        """Creates A dataframe from the user input it uses the best features
            for each model and set it as a dataframe
            Need to understand that the each model has diffrent features.
        Returns:
            DataFrame: Dataframe for the prediction function.
        """
        d = {}
        features = self.chosen_model.getFeatures()  # Gets the best features
        for feature in features:
            if feature in self.features:
                d[feature] = [self.features[feature]]  # Create a dynamic Dict

        df = pd.DataFrame(data=d)  # Convert the dict to a dataframe
        return df

    def __chooseModel(self):
        """ Flaged as a private function, as it should be only used in the class.
            The function gets the correct paramaters from Model_Path_Dict and
            returns the model.
        Returns:
            Model: Model
        """
        is_weekend = self.__isWeekEnd()  # Returns weekday or weekend
        get_time = self.__getDayRange()  # Returns Morning / night .. etc
        model = MODEL_PATH_DICT.get('summer', {}).get(
            is_weekend).get(get_time, {})  # Gets the Model from the dict
        return model

    def __isWeekEnd(self):
        """ Flaged as private function, uses the Date to understand if it a
            weekday or weekend.
        Returns:
            Str: Returns Weekend or Weekday.
        """
        input_date = datetime.strptime(self.date, "%d/%m/%Y")
        weekend_list = ['Friday', 'Sunday', 'Saturday']
        if input_date in weekend_list:
            return 'weekend'
        return 'weekday'

    def __getDayRange(self):
        """ Flaged as private function, uses the Time to understand if its a
            morning, night, midnight or noon
        Returns:
            Str: Returns the correct path.
        """
        h, m = self.time.split(':')
        if '00' <= h <= '06':
            return 'midnight'
        if '07' <= h <= '11':
            return 'morning'
        if '12' <= h <= '19':
            return 'afternoon'
        else:
            return 'night'


class ModelMetaData:
    """ ModelMetaData is a class which olds the path for the model.
        and has a function which returns the Best_Feature.
    """

    def getFeatures(self) -> List[str]:
        """ Gets the best feature from a saved file and returns it as a list

        Returns:
            List[str]: contains the label of the features
        """
        with open(self.path + r'\best_features.txt', 'r') as f:
            return f.read().splitlines()

    def __init__(self, folder_name: str) -> None:
        """ Constructor for class, gets the file name and set the path

        Args:
            folder_name (str): the name of the folder which contain the folder
        """
        self.path = os.path.join(r'..\..\models_data', folder_name)
        print(self.path, file=sys.stderr)


# CONST
MODEL_PATH_DICT: Final[dict] = {
    'summer': {
        'weekday': {
            'morning': ModelMetaData(r'summer_mid_week_morning_df'),
            'afternoon': ModelMetaData(r'summer_mid_week_noon_afternoon_df'),
            'night': ModelMetaData(r'summer_mid_week_night_df'),
            'midnight': ModelMetaData(r'summer_mid_week_midnight_df')
        },
        'weekend': {
            'morning': ModelMetaData(r'summer_week_end_morning_df'),
            'afternoon': ModelMetaData(r'summer_week_end_noon_afternoon_df'),
            'night': ModelMetaData(r'summer_week_end_night_df'),
            'midnight': ModelMetaData(r'summer_week_end_midnight_df')
        }
    },
    'spring': {
        'weekday': {
            'morning': ModelMetaData(r'spring_mid_week_morning_df'),
            'afternoon': ModelMetaData(r'spring_mid_week_noon_afternoon_df'),
            'night': ModelMetaData(r'spring_mid_week_night_df'),
            'midnight': ModelMetaData(r'spring_mid_week_midnight_df')
        },
        'weekend': {
            'morning': ModelMetaData(r'spring_week_end_morning_df'),
            'afternoon': ModelMetaData(r'spring_week_end_noon_afternoon_df'),
            'night': ModelMetaData(r'spring_week_end_night_df'),
            'midnight': ModelMetaData(r'spring_week_end_midnight_df')
        }
    },
    'fall': {
        'weekday': {
            'morning': ModelMetaData(r'fall_mid_week_morning_df'),
            'afternoon': ModelMetaData(r'fall_mid_week_noon_afternoon_df'),
            'night': ModelMetaData(r'fall_mid_week_night_df'),
            'midnight': ModelMetaData(r'fall_mid_week_midnight_df')
        },
        'weekend': {
            'morning': ModelMetaData(r'fall_week_end_morning_df'),
            'afternoon': ModelMetaData(r'fall_week_end_noon_afternoon_df'),
            'night': ModelMetaData(r'fall_week_end_night_df'),
            'midnight': ModelMetaData(r'fall_week_end_midnight_df')
        }
    },
    'winter': {
        'weekday': {
            'morning': ModelMetaData(r'winter_mid_week_morning_df'),
            'afternoon': ModelMetaData(r'winter_mid_week_noon_afternoon_df'),
            'night': ModelMetaData(r'winter_mid_week_night_df'),
            'midnight': ModelMetaData(r'winter_mid_week_midnight_df')
        },
        'weekend': {
            'morning': ModelMetaData(r'winter_week_end_morning_df'),
            'afternoon': ModelMetaData(r'winter_week_end_noon_afternoon_df'),
            'night': ModelMetaData(r'winter_week_end_night_df'),
            'midnight': ModelMetaData(r'winter_week_end_midnight_df')
        }
    }
}
