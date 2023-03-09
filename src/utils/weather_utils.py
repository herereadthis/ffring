import requests
import re
import xml.etree.ElementTree as ET
import datetime as dt


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


def get_weather_data(airport):
    """
    Get the current weather data from a specified URL and return as a dictionary
    """
    weather_url = f'https://w1.weather.gov/xml/current_obs/{airport}.xml'
    also_weather_url = 'https://api.weather.gov/gridpoints/LWX/91,70/forecast'
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

    return weather_report