from flask import Flask
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
data = [{
        'name': "Chelsea",
        'values': [
            {'label': "Population", 'val': 20000},
            {'label': "Restaurants", 'val': "690"},
        ],
        'color': "#E31A1C",
        }]


@ app.route('/books')
def index():
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
