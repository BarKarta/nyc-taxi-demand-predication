from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return [{
        'name': "Chelsea",
        'values': [
            {'label': "Population", 'val': 20000},
            {'label': "Restaurants", 'val': "690"},
        ],
        'color': "#E31A1C",
    }]


if __name__ == '__main__':
    app.run(debug=True)
