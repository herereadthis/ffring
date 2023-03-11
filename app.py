import json
from src.utils import weather_utils, dump1090_utils
import uuid

from flask import Flask, jsonify, render_template, session
app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

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
    receiver_options = dump1090_utils.get_receiver_options(base_adsb_url)
    base_lat = receiver_options["lat"]
    base_lon = receiver_options["lon"]

    forecast_hourly_url, local_timezone = weather_utils.get_grid_data(base_lat, base_lon)

    if (session.get('forcast_hourly_url') is None or session.get('local_timezone') is None):
        forecast_hourly_url, local_timezone = weather_utils.get_grid_data(base_lat, base_lon)
        session['forcast_hourly_url'] = forecast_hourly_url
        session['local_timezone'] = local_timezone

    weather_report = weather_utils.get_weather_data(session.get('forcast_hourly_url'), session.get('local_timezone'))
    aircraft_list = dump1090_utils.get_aircraft(base_adsb_url, base_lat, base_lon)

    print(session.get('local_timezone'))

    stuff['weather_report'] = weather_report
    stuff['receiver_options'] = receiver_options
    stuff['aircraft_list'] = aircraft_list
    stuff['local_timezone'] = session.get('local_timezone')

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

