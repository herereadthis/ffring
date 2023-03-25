import uuid
import adsb_tools.timezone
import adsb_tools.receiver
from adsb_tools.aircraft import Aircraft
from adsb_tools.receiver import Receiver
import adsb_tools.weather
# from pprint import pprint
from flask import Flask, render_template, session, request
from src.utils.flask_utils import return_json

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
        'ffring_aircraft': {
            'label': 'Ffring Aircraft',
            'url': 'aircraft'
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
    receiver = Receiver(base_adsb_url)
    base_lat = receiver.lat
    base_lon = receiver.lon

    if (session.get('local_timezone_name') is None):
        local_timezone = adsb_tools.timezone.get_timezone_name(base_lat, base_lon)
        session['local_timezone_name'] = local_timezone

    if (session.get('forcast_hourly_url') is None or session.get('weather_timezone_name') is None):
        print('Weather grid data not found. Getting grid data.')
        forecast_hourly_url, weather_timezone_name = adsb_tools.weather.get_grid_data(base_lat, base_lon)
        print(f"forecast_hourly_url: {forecast_hourly_url}")
        print(f"weather_timezone_name: {weather_timezone_name}")
        session['forcast_hourly_url'] = forecast_hourly_url
        session['weather_timezone_name'] = weather_timezone_name
    else:
        print('Weather grid data exists in current session.')

    weather_report = adsb_tools.weather.get_weather_data(
        # There should be only one source of truth for timezone name!
        session.get('forcast_hourly_url'), session.get('weather_timezone_name')
    )

    aircraft = Aircraft(base_adsb_url, base_lat, base_lon)
    icao_24 = aircraft.nearest_aircraft['icao_24']

    session_icao = session.get('nearest_aircraft', {}).get('icao_24')
    print(f"\nPrevious session icao is: {session_icao}")
    print(f"Current nearest_aircraft_icao is: {icao_24}")

    if (not session_icao or session_icao != icao_24):
        print('Storing new aircraft into session...\n')
        aircraft.retrieve_external_aircraft_options()
    else:
        print('Session shall continue with current aircraft...\n')
        aircraft.map_static_aircraft_options(session.get('nearest_aircraft'))
    session['nearest_aircraft'] = aircraft.nearest_aircraft

    params = {
        'system': stuff['system'],
        'weather_report': weather_report,
        'receiver': receiver,
        'local_timezone_name': session.get('local_timezone_name'),
        'nearest_aircraft': session.get('nearest_aircraft')
    }
    params['system']['ffring_aircraft']['url'] = f"{request.url_root}aircraft"

    return render_template('index.html', **params)


@app.route('/aircraft', methods=['GET'])
@return_json
def get_all_aircraft():
    """
    Returns JSON of all aircraft messges, augmented with options.
    """
    receiver = Receiver(base_adsb_url)
    aircraft = Aircraft(base_adsb_url, receiver.lat, receiver.lon)
    print(aircraft.aircraft_list)

    return aircraft.aircraft_list


# @app.route('/users/<username>')
# def get_user(username):
#     with open('static/users.json') as f:
#         users = json.load(f)
#         user = users.get(username)
#         if user is None:
#             return jsonify({'error': 'User not found'}), 404
#         return jsonify(user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8083", debug=True)

