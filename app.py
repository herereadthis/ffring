import json
from src.utils import weather_utils, dump1090_utils

from flask import Flask, jsonify, render_template
app = Flask(__name__)

weather_url = 'https://w1.weather.gov/xml/current_obs/KDCA.xml'

base_adsb_url = 'http://adsb.local:8080'

stuff = {
    'aircraft_json_url': f'{base_adsb_url}/data/aircraft.json',
    'title': 'FFring!',
    'urls': [
        {
            'name': 'Receiver JSON',
            'url': f'{base_adsb_url}/data/receiver.json'
        },
        {
            'name': 'Stats JSON',
            'url': f'{base_adsb_url}/data/stats.json'
        },
        {
            'name': 'Aircraft JSON',
            'url': f'{base_adsb_url}/data/aircraft.json'
        },
        {
            'name': 'Tar1090',
            'url': f'{base_adsb_url}/tar1090'
        },
        {
            'name': 'Graphs1090',
            'url': f'{base_adsb_url}/graphs1090'
        },
        {
            'name': 'PiAware',
            'url': f'{base_adsb_url}/'
        }
    ]
}


@app.route('/')
def get_index():
    weather_report = weather_utils.get_weather_data('KDCA')
    receiver_options = dump1090_utils.get_receiver_options(base_adsb_url)

    stuff['weather_report'] = weather_report
    stuff['receiver_options'] = receiver_options

    return render_template('index.html', **stuff)


@app.route('/users/<username>')
def get_user(username):
    with open('static/users.json') as f:
        users = json.load(f)
        user = users.get(username)
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8083", debug=True)

