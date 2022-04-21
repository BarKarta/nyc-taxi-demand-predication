import pickle
from typing import Final, List
import os


class MyModel:
    def __init__(self, features: dict) -> None:
        self.features = features
        model_path = os.join(MODEL_PATH_DICT.get('winter', {})
                             .get('weekday', {}).get('morning', {}),
                             'ML_model.sav')
        with open(model_path, 'rb') as f:
            self.loaded_model = pickle.load(f)

    def runModel(self):
        self.loaded_model.predict(self.features)

    def chooseModel(self):

        return 'str'


class ModelMetaData:
    def getFeatures(self):
        with open(self.path, 'r') as f:
            return f.readlines()

    def __init__(self, folder_name: str) -> None:
        self.path = os.path.join(r'..\..\models_data', folder_name)


# CONST
MODEL_PATH_DICT: Final[dict] = {
    'summer': {
        'weekday': {
            'morning': ModelMetaData(r'weekday_morning'),
            'afternoon': 'path2',
            'night': 'path3',
            'midnight': 'path4'
        },
        'weekend': {
            'morning': 'path1',
            'afternoon': 'path2',
            'night': 'path3',
            'midnight': 'path4'
        }
    },
    'spring': {
        'weekday': {
            'morning': 'path1',
            'afternoon': 'path2',
            'night': 'path3',
            'midnight': 'path4'
        },
        'weekend': {
            'morning': 'path1',
            'afternoon': 'path2',
            'night': 'path3',
            'midnight': 'path4'
        }
    },
    'fall': {
        'weekday': {
            'morning': 'path1',
            'afternoon': 'path2',
            'night': 'path3',
            'midnight': 'path4'
        },
        'weekend': {
            'morning': 'path1',
            'afternoon': 'path2',
            'night': 'path3',
            'midnight': 'path4'
        }
    },
    'winter': {
        'weekday': {
            'morning': 'path1',
            'afternoon': 'path2',
            'night': 'path3',
            'midnight': 'path4'
        },
        'weekend': {
            'morning': 'path1',
            'afternoon': 'path2',
            'night': 'path3',
            'midnight': 'path4'
        }
    }
}

# class DayRange:
#     def __init__(self, morning: ModelMetaData, afternoon: ModelMetaData,
#                  night: ModelMetaData, midnight: ModelMetaData) -> None:
#         self.morning = morning
#         self.afternoon = afternoon
#         self.night = night
#         self.midnight = midnight


# class WeekRange:
#     def __init__(self,) -> None:
#         pass


# class Seasons:
#     def __init__(self, summer: DayRange, winter: DayRange, fall: DayRange,
#                  spring: DayRange) -> None:
#         self.summer = summer
#         self.winter = winter
#         self.fall = fall
#         self.spring = spring
