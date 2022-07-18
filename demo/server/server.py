from utility import data_prep_functions as ut
import json
from typing import Final, List
from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
import requests
from datetime import datetime
import calendar


from MyModel import MyModel
import sys
sys.path.append("../..")

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


zones_to_name_dict: Final = {
    "Inwood": [153, 128, 127],
    "Washington Heights": [120, 244],
    "Hamilton Heights": [116, 152],
    "Central Harlem": [42, 41],
    "Morningside Heights": [166],
    "Upper West Side": [24, 151, 238, 239, 143, 142],
    "Central Park": [43],
    "Spanish Harlem": [74, 75],
    "Randall's Island": [194],
    "Upper East Side": [236, 263, 262, 237, 141, 140],
    "Roosevelt Island": [202],
    "Midtown West": [50, 48, 163, 230, 161, 100, 164],
    "Midtown East": [170, 162, 229, 233, 170],
    "Kips Bay": [137],
    "Stuyvesant Town": [224],
    "Chelsea": [246, 68, 90],
    "Flatiron District": [186],
    "West Village": [158, 249],
    "Greenwich Village": [113, 114],
    "East Village": [79, 4],
    "Soho": [125, 221, 144],
    "Lower East Side": [148, 232],
    "Tribeca": [231],
    "Two Bridges": [45],
    "Battery Park City": [13, 12],
    "Financial District": [209, 261, 87, 88, 12]
}


def getInfo(data, input_key):
    for key in data:
        if key == input_key:
            return data[input_key].get("1h")
        else:
            return 0


def setWeatherData(res: json, time: str) -> dict:

    data = res['hourly']
    time = datetime.strptime(time, "%H:%M")
    current_time = datetime.now()
    time_delta = time - current_time
    if time_delta.seconds//3600 > 48:
        return
    data = data[time_delta.seconds//3600]
    return {
        "Tmax": data["temp"],
        "Tmin": data["feels_like"],
        "Tavg": ((data["temp"] + data["feels_like"])/2),
        "Tdep": 0,
        "HDD": 0,
        "CDD": 0,
        "Precipitation": getInfo(data, 'rain'),
        "new_snow": getInfo(data, 'snow'),
        "snow_depth": getInfo(data, 'snow')
    }


def getWeather(time: str) -> dict:
    API_KEY: Final[str] = '122b5198256253814e7bb22a9e9da50f'
    LAT: Final[float] = 40.7834
    LON: Final[float] = -73.9662
    EXCLUDE: Final[list] = ['minutely', 'daily', 'alerts']
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={LAT}&lon={LON}&exclude={EXCLUDE}&units=metric&appid={API_KEY}'
    response = requests.get(url).json()
    dict = setWeatherData(response, time)
    return dict


def getTimeBinned(time: str) -> dict:
    h, m = time.split(':')
    h = str(h)
    input = f'{h:02}:00 - {h:02}:59'
    label_list = ut.get_hours_label(0, 24)
    dict = {}
    for label in label_list:
        if label == input:
            dict[label] = 1
        else:
            dict[label] = 0
    return dict


def getWeekDay(date: datetime) -> dict:
    input_date = datetime.strptime(date, "%d/%m/%Y")
    input_day = calendar.day_name[input_date.weekday()]
    days = [day for day in calendar.day_name]
    dict = {}
    for day in days:
        if input_day == day:
            dict[day] = 1
        else:
            dict[day] = 0
    return dict


def getZoneIDs(zone_name: List[str]) -> dict:
    dict = {}
    for zone in zone_name:
        dict[zone] = zones_to_name_dict[zone]
    return dict


def setUpModels(zone_id: dict, time_binned: dict, weekday: dict,
                weather_data: dict, time, date):
    dict_list = []
    for key, value in zone_id.items():
        number_of_taxis = 0
        data = {}
        for val in value:
            features = {**time_binned, **weekday, **weather_data}
            features["Zone"] = val
            model = MyModel(features, time, date)
            temp = model.runModel()
            number_of_taxis += temp[0]

        data = {
            'name': key,
            'values':
            [
                {
                    'label': "Number of Drives",
                    'val': int(number_of_taxis)
                }
            ],
            'color': "#E31A1C",
        }
        dict_list.append(data)
    return dict_list


@ app.route('/calc', methods=['POST'])
def get_input():

    zone = request.json['zone']
    date = request.json['date']
    time = request.json['time']

    zone_id = getZoneIDs(zone)
    time_binned = getTimeBinned(time)
    weekday = getWeekDay(date)
    weather_data = getWeather(time)
    return jsonify(setUpModels(zone_id, time_binned, weekday,
                               weather_data, time, date))


if __name__ == '__main__':
    app.run(debug=True)
