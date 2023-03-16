import json
from src.utils import dump1090_utils
import uuid
import adsb_tools.timezone
import adsb_tools.receiver
import adsb_tools.aircraft
import adsb_tools.weather
from pprint import pprint

from flask import Flask, jsonify, render_template, session

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

base_adsb_url = 'http://adsb.local:8080'

stuff = {
    'system': {
        'tar1090': {
            'label': 'Tar1090',
            'url': f'{base_adsb_url}/tar1090'
        },
        'graphs1090': {
            'label': 'Graphs1090',
            'url': f'{base_adsb_url}/graphs1090'
        },
        'piaware': {
            'label': 'PiAware',
            'url': f'{base_adsb_url}'
        },
        'urls': {
            'aircraft': f'{base_adsb_url}/data/aircraft.json',
            'stats': f'{base_adsb_url}/data/stats.json',
            'receiver': f'{base_adsb_url}/data/receiver.json'
        },
        'title': 'FFring!'
    }
}


@app.route('/')
def get_index():
    receiver_options = adsb_tools.receiver.get_receiver(base_adsb_url)
    base_lat = receiver_options["lat"]
    base_lon = receiver_options["lon"]

    if (session.get('local_timezone_name') is None):
        local_timezone = adsb_tools.timezone.get_timezone_name(base_lat, base_lon)
        session['local_timezone_name'] = local_timezone

    print(12345)
    if (session.get('forcast_hourly_url') is None or session.get('weather_timezone') is None):
        forecast_hourly_url, weather_timezone_name = adsb_tools.weather.get_grid_data(base_lat, base_lon)
        print('forecast_hourly_url')
        print(forecast_hourly_url)
        print('weather_timezone_name')
        print(forecast_hourly_url)
        session['forcast_hourly_url'] = forecast_hourly_url
        session['weather_timezone_name'] = weather_timezone_name

    weather_report = adsb_tools.weather.get_weather_data(
        # There should be only one source of truth for timezone name!
        session.get('forcast_hourly_url'), session.get('weather_timezone_name')
    )
    pprint(weather_report)

    aircraft_list = dump1090_utils.get_aircraft(base_adsb_url, base_lat, base_lon)

    nearest_aircraft = aircraft_list[0]
    icao_24 = nearest_aircraft['icao']
    nearest_aircraft['hexdb'] = {
        'aircraft_url': f'https://hexdb.io/api/v1/aircraft/{icao_24}',
        'conversion_url': f'https://hexdb.io/hex-reg?hex={icao_24}'
    }
    nearest_aircraft['adsb_db'] = {
        'aircraft_url': f'https://api.adsbdb.com/v0/aircraft/{icao_24}',
        'conversion_url': f'https://api.adsbdb.com/v0/mode-s/{icao_24}'
    }

    session_icao = session.get('nearest_aircraft', {}).get('icao')
    aircraft_image = {}
    print(f"\nPrevious session icao is: {session_icao}")
    print(f"Current nearest_aircraft_icao is: {icao_24}")

    if (not session_icao or session_icao != icao_24):
        print('Storing new aircraft into session...\n')
        if (icao_24):
            aircraft_image = adsb_tools.aircraft.get_aircraft_image(icao_24)
            nearest_aircraft['image'] = aircraft_image
        session['nearest_aircraft'] = nearest_aircraft
    else:
        print('Session shall continue with current aircraft...\n')
        aircraft_image = session.get('nearest_aircraft', {}).get('image')

    stuff['weather_report'] = weather_report
    stuff['receiver_options'] = receiver_options
    stuff['aircraft_list'] = aircraft_list
    stuff['local_timezone_name'] = session.get('local_timezone_name')
    stuff['aircraft_image'] = aircraft_image
    stuff['nearest_aircraft'] = session.get('nearest_aircraft')

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

