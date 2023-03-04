import json
import requests
import re
import xml.etree.ElementTree as ET
import datetime as dt

from flask import Flask, jsonify, render_template
app = Flask(__name__)

weather_url = 'https://w1.weather.gov/xml/current_obs/KDCA.xml'

base_adsb_url = 'http://adsb.local:8080'

stuff = {
    'aircraft_json_url': f'{base_adsb_url}/data/aircraft.json',
    'title': 'FFring!',
    'urls': [
        {
            'name': 'aircraft JSON',
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


def get_tag_value(root, loc):
    text = root.find(f'.//{loc}').text.strip()
    # from https://www.regextester.com/104184
    regex = '^-?([0]{1}\.{1}[0-9]+|[1-9]{1}[0-9]*\.{1}[0-9]+|[0-9]+|0)$'
    if re.match(regex, text) == None:
        result = text
    else:
        result = float(text)
    return result


def get_datetime_string(ts):
    return ts.strftime('%Y-%m-%dT%H:%M:%S%z')


@app.route('/')
def hello_geek():
    weather_response = requests.get(weather_url)
    root = ET.fromstring(weather_response.content)

    observation_time_rfc822 = get_tag_value(root, 'observation_time_rfc822')
    formatted_ts = dt.datetime.strptime(observation_time_rfc822, '%a, %d %b %Y %H:%M:%S %z')

    weather_report = {
        'observation_ts': get_datetime_string(formatted_ts),
        'observation_readable': formatted_ts.strftime('%I:%M%p on %a, %d %b'),
        'weather': get_tag_value(root, 'weather'),
        'temp_f': get_tag_value(root, 'temp_f'),
        'temp_c': get_tag_value(root, 'temp_c'),
        'relative_humidity': get_tag_value(root, 'relative_humidity'),
        'wind_dir': get_tag_value(root, 'wind_dir'),
        'wind_degrees': get_tag_value(root, 'wind_degrees'),
        'wind_mph': get_tag_value(root, 'wind_mph'),
        'wind_kt': get_tag_value(root, 'wind_kt'),
        'pressure_mb': get_tag_value(root, 'pressure_mb'),
        'pressure_in': get_tag_value(root, 'pressure_in'),
        'dewpoint_f': get_tag_value(root, 'dewpoint_f'),
        'dewpoint_c': get_tag_value(root, 'dewpoint_c'),
        'visibility_mi': get_tag_value(root, 'visibility_mi')
    }

    stuff['weather_report'] = weather_report

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

