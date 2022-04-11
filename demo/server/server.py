import json
import string
from tokenize import String
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from flask import request
from datetime import datetime
import calendar

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
data = [{
        'name': "Chelsea",
        'values': [
            {'label': "Number of Drives", 'val': 100},
        ],
        'color': "#E31A1C",
        }]

zones_to_name_dict = {
    "Inwood": ["153", "128", "127"],
    "Washington Heights": ["120", "244"],
    "Hamilton Heights": ["116", "152"],
    "Central Harlem": ["42", "41"],
    "Morningside Heights": ["166"],
    "Upper West Side": ["24", "151", "238", "239", "143", "142"],
    "Central Park": ["43"],
    "Spanish Harlem": ["74", "75"],
    "Randall's Island": ["194"],
    "Upper East Side": ["236", "263", "262", "237", "141", "140"],
    "Roosevelt Island": ["202"],
    "Midtown West": ["50", "48", "163", "230", "161", "100", "164"],
    "Midtown East": ["170", "162", "229", "233", "170"],
    "Kips Bay": ["137"],
    "Stuyvesant Town": ["224"],
    "Chelsea": ["246", "68", "90"],
    "Flatiron District": ["186"],
    "West Village": ["158", "249"],
    "Greenwich Village": ["113", "114"],
    "East Village": ["79", "4"],
    "Soho": ["125", "221", "144"],
    "Lower East Side": ["148", "232"],
    "Tribeca": ["231"],
    "Two Bridges": ["45"],
    "Battery Park City": ["13", "12"],
    "Financial District": ["209", "261", "87", "88", "12"]
}


def getWeather(date: String, time: String):

    # TODO MAKE FUNCTION
    return 1


def getTimeBinned(time):
    # TODO MAKE FUNCTION
    return 1


def getWeekDay(date):
    my_date = datetime.strptime(date, "%d/%m/%Y")
    return calendar.day_name[my_date.weekday()]


def getZoneName(zone):
    for key in zones_to_name_dict:
        if zone in zones_to_name_dict[key]:
            zone_name = key
    return zone_name


@app.route('/calc', methods=['POST'])
def get_input():

    zone = request.json['zone']
    date = request.json['date']
    time = request.json['time']
    # # TODO Add the API and get the weather information needed, based on the data we are getting from the user
    # temp_man, temp_min, hdd, cdd, precipitation, new_snow, snow_depth = getWeather(
    #     date, time)
    # # TODO Convert the Time to a interval
    # time_binned = getTimeBinned(time)
    weekday = getWeekDay(date)
    zone_name = getZoneName(zone)
    return jsonify(f'Zone : {zone}, Date : {date}, Time : {time},WeekDay: {weekday},Zone Name : {zone_name}')


if __name__ == '__main__':
    app.run(debug=True)
