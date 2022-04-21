
from typing import Final, List
from flask import Flask, jsonify
from flask_cors import CORS
from flask import request
import requests
from datetime import datetime
import calendar

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# data = [{
#         'name': "Chelsea",
#         'values': [
#             {'label': "Number of Drives", 'val': 100},
#         ],
#         'color': "#E31A1C",
#         }]

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


def getWeather():
    API_KEY: Final[str] = '122b5198256253814e7bb22a9e9da50f'
    LAT: Final[float] = 40.7834
    LON: Final[float] = -73.9662
    EXCLUDE: Final[list] = ['minutely', 'daily', 'alerts']
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={LAT}&lon={LON}&exclude={EXCLUDE}&units=metric&appid={API_KEY}'
    response = requests.get(url).json()
    return response


def getTimeBinned(time: str):
    h, m = time.split(':')
    h = str(h)
    return f'{h:02}:00 - {h:02}:59'


def getWeekDay(date: datetime):
    my_date = datetime.strptime(date, "%d/%m/%Y")
    return calendar.day_name[my_date.weekday()]


def getZoneIDs(zone_name: List[str]):

    return zones_to_name_dict.get(zone_name[0])


# def calcModel(zone,weekday,time_binned):


@app.route('/calc', methods=['POST'])
def get_input():

    zone = request.json['zone']
    date = request.json['date']
    time = request.json['time']
    time_binned = getTimeBinned(time)
    zone_id = getZoneIDs(zone)
    getWeather()
    weekday = getWeekDay(date)

    return jsonify(f'{zone_id}, {date}, {time_binned}, {weekday}')


if __name__ == '__main__':
    app.run(debug=True)
