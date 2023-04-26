# import uuid
from jinja2 import Environment, FileSystemLoader
import adsb_tools.timezone
import adsb_tools.receiver
from adsb_tools.aircraft import Aircraft
from adsb_tools.receiver import Receiver
from adsb_tools.wake_vortex import WakeVortexCategories
from adsb_tools.utils import dt_utils
import adsb_tools.weather
# from pprint import pprint
from flask import Flask, render_template, session, request, url_for
from src.utils.flask_utils import return_json
from src.utils.session_utils import get_config

app = Flask(__name__)
# app.secret_key = str(uuid.uuid4())
# static secret key shall persist session in debug mode
app.secret_key = '53d1e164-9dff-4aa4-912d-ad00903862d4'
# app.secret_key = str(uuid.uuid4())

BASE_ADSB_URL = 'http://adsb.local:8080'

stuff = {
    'system': {
        'tar1090': {
            'label': 'Tar1090',
            'url': f'{BASE_ADSB_URL}/tar1090'
        },
        'graphs1090': {
            'label': 'Graphs1090',
            'url': f'{BASE_ADSB_URL}/graphs1090'
        },
        'piaware': {
            'label': 'PiAware',
            'url': f'{BASE_ADSB_URL}'
        },
        'ffring_aircraft': {
            'label': 'Ffring Aircraft',
            'url': 'aircraft'
        },
        'ffring_aircraft_nearest': {
            'label': 'Ffring Nearest Aircraft',
            'url': 'aircraft/nearest'
        },
        'ffring_wtc': {
            'label': 'Wake Vortex Categories',
            'url': 'wtc'
        },
        'urls': {
            'aircraft': f'{BASE_ADSB_URL}/data/aircraft.json',
            'stats': f'{BASE_ADSB_URL}/data/stats.json',
            'receiver': f'{BASE_ADSB_URL}/data/receiver.json'
        },
        'title': 'FFring'
    }
}


def render_schedule_diff(value):
    print(f'schedule_diff: {value}')
    result = ''
    if value < 0:
        result = f'<div class="schedule_early">{abs(value)} minutes early</div>'
    else:
        result = f'<div class="schedule_delayed">{value} minutes delayed</div>'
    return result

def render_or_unknown(dict_to_check, key, unknown = 'unknown'):
    result = unknown
    if dict_to_check is None or len(dict_to_check) == 0:
        result = unknown
    elif key not in dict_to_check or dict_to_check[key] is None or len(dict_to_check[key]) == 0:
        result = unknown
    else:
        print('dict_to_check')
        print(dict_to_check)
        result = dict_to_check[key]
    return result

def render_flightaware(flightaware, local_timezone_name):
    if flightaware is None or len(flightaware) == 0:
        return '<div/>'
    else:
        template = env.get_template('flightaware.html')
        flightaware['local_timezone_name'] = local_timezone_name
        output = template.render(**flightaware)
        return output

def render_weather(weather_report):
    if weather_report is None or len(weather_report) == 0:
        return '<div/>'
    else:
        template = env.get_template('weather.html')
        output = template.render(**weather_report)
        return output

def get_time_diff_class(actual_time, scheduled_time):
    td_class = 'equal'
    if (actual_time is not None and scheduled_time is not None):
        time_diff = dt_utils.compare_datetimes(actual_time, scheduled_time)
        if time_diff == -1:
            td_class = 'early'
        elif time_diff == 1:
            td_class = 'delayed'
    
    return td_class
        

env = Environment(loader=FileSystemLoader('templates'))
env.filters['format_datetime'] = dt_utils.format_datetime
env.filters['format_date_short'] = dt_utils.format_date_short
env.filters['format_time_short'] = dt_utils.format_time_short
env.filters['format_tz'] = dt_utils.format_tz
env.filters['render_schedule_diff'] = render_schedule_diff
env.filters['render_or_unknown'] = render_or_unknown
env.filters['render_flightaware'] = render_flightaware
env.filters['render_weather'] = render_weather
env.filters['get_time_diff_class'] = get_time_diff_class

def add_flask_built_ins(context):
    context['url_for'] = url_for
    return context


@app.route('/')
def get_index():
    config = get_config()

    flightware_api_key = config.get('api_keys', {}).get('flightaware', '')

    receiver = Receiver(BASE_ADSB_URL)
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

    aircraft = Aircraft(BASE_ADSB_URL, base_lat, base_lon, flightware_api_key)
    icao_24 = aircraft.nearest_aircraft['icao_24']

    session_icao = session.get('nearest_aircraft', {}).get('icao_24')
    print(f"\nPrevious session icao is: {session_icao}")
    print(f"Current nearest_aircraft_icao is: {icao_24}")

    if (not session_icao or session_icao != icao_24):
        print('Storing new aircraft into session...\n')
        aircraft.retrieve_external_aircraft_options()
        flightaware = aircraft.set_flightaware_ident()
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
    params['system']['ffring_aircraft_nearest']['url'] = f"{request.url_root}aircraft/nearest"
    params['system']['ffring_wtc']['url'] = f"{request.url_root}wtc"
    add_flask_built_ins(params)

    template = env.get_template('index.html')
    output = template.render(**params)
    return output


@app.route('/aircraft', methods=['GET'])
@return_json
def get_all_aircraft():
    """
    Returns JSON of all aircraft messges, augmented with options.
    """
    receiver = Receiver(BASE_ADSB_URL)
    aircraft = Aircraft(BASE_ADSB_URL, receiver.lat, receiver.lon)
    print(aircraft.aircraft_list)

    return aircraft.aircraft_list

@app.route('/aircraft/nearest', methods=['GET'])
@return_json
def get_all_closes_aircraft():
    """
    Returns JSON of all aircraft messges, augmented with options.
    """
    config = get_config()
    flightware_api_key = config.get('api_keys', {}).get('flightaware', '')

    receiver = Receiver(BASE_ADSB_URL)
    aircraft = Aircraft(BASE_ADSB_URL, receiver.lat, receiver.lon, flightware_api_key)

    icao_24 = aircraft.nearest_aircraft['icao_24']

    session_icao = session.get('nearest_aircraft', {}).get('icao_24')
    print(f"\nPrevious session icao is: {session_icao}")
    print(f"Current nearest_aircraft_icao is: {icao_24}")

    if (not session_icao or session_icao != icao_24):
        print('Storing new aircraft into session...\n')
        aircraft.retrieve_external_aircraft_options()
        flightaware = aircraft.set_flightaware_ident()
    else:
        print('Session shall continue with current aircraft...\n')
        aircraft.map_static_aircraft_options(session.get('nearest_aircraft'))
    session['nearest_aircraft'] = aircraft.nearest_aircraft

    return session['nearest_aircraft']


@app.route('/wtc', methods=['GET'])
@return_json
def get_wake_vortex_categories():
    """
    Returns JSON of a list of wake vortex categories.
    """
    wtc = WakeVortexCategories()
    return wtc.categories


@app.route('/wtc/<category>', methods=['GET'])
@return_json
def get_wake_vortex_category(category):
    """
    Returns JSON of a list of wake vortex categories.
    """
    wtc = WakeVortexCategories()
    return wtc.get_category_dict(category)


@app.route('/weather/base', methods=['GET'])
@return_json
def get_weather():
    receiver = Receiver(BASE_ADSB_URL)
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

    return weather_report


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8083", debug=True)

