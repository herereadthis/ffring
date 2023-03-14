import json
from src.utils import weather_utils, dump1090_utils
import uuid
import time
import adsb_tools.timezone
import adsb_tools.receiver
import adsb_tools.aircraft
from pprint import pprint

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
    receiver_options = adsb_tools.receiver.get_receiver(base_adsb_url)
    base_lat = receiver_options["lat"]
    base_lon = receiver_options["lon"]

    if (session.get('local_timezone_name') is None):
        local_timezone = adsb_tools.timezone.get_timezone_name(base_lat, base_lon)
        session['local_timezone_name'] = local_timezone

    if (session.get('forcast_hourly_url') is None or session.get('weather_timezone') is None):
        forecast_hourly_url, weather_timezone_name = weather_utils.get_grid_data(base_lat, base_lon)
        session['forcast_hourly_url'] = forecast_hourly_url
        session['weather_timezone_name'] = weather_timezone_name

    weather_report = weather_utils.get_weather_data(
        # There should be only one source of truth for timezone name!
        session.get('forcast_hourly_url'), session.get('weather_timezone_name')
    )
    aircraft_list = dump1090_utils.get_aircraft(base_adsb_url, base_lat, base_lon)

    nearest_aircraft = aircraft_list[0]
    icao_24 = nearest_aircraft['icao']
    nearest_aircraft['hexdb'] = {
        'aircraft_url': f'https://hexdb.io/api/v1/aircraft/{icao_24}',
        'conversion_url': f'https://hexdb.io/hex-reg?hex={icao_24}'
    }
    print(f"nearest_aircraft_icao is {icao_24}")

    aircraft_image = {}

    if (not session.get('nearest_aircraft.icao') or session.get('nearest_aircraft.icao') != icao_24):
        print('nearest aircraft not previously detected')
        session['nearest_aircraft'] = nearest_aircraft
        if (icao_24):
            aircraft_image = adsb_tools.aircraft.get_aircraft_image(icao_24)
            session['nearest_aircraft']['image'] = aircraft_image
    else:
        print('still following the same nearest aircraft')
        aircraft_image = session.get('nearest_aircraft.image', {})

    pprint(session)


    stuff['weather_report'] = weather_report
    stuff['receiver_options'] = receiver_options
    stuff['aircraft_list'] = aircraft_list
    stuff['local_timezone_name'] = session.get('local_timezone_name')
    stuff['aircraft_image'] = aircraft_image
    stuff['nearest_aircraft'] = session.get('nearest_aircraft')

    pprint(stuff['nearest_aircraft'])

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

