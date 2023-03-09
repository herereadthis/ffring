import json
import requests
import re
# import datetime as dt
# from pprint import pprint


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


def get_weather_data(airport, latitude, longitude):
    """
    Get the current weather data from a specified URL and return as a dictionary
    """
    get_grid_url = f'https://api.weather.gov/points/{latitude},{longitude}'
    # also_weather_url = 'https://api.weather.gov/gridpoints/LWX/91,70/forecast/hourly'

    grid_response = requests.get(get_grid_url)
    grid_json_obj = json.loads(grid_response.content)
    print('retrieved grid response.')
    forecastHourlyUrl = grid_json_obj['properties']['forecastHourly']

    weather_response = requests.get(forecastHourlyUrl)
    weather_json_obj = json.loads(weather_response.content)
    print('retrieved weather response.')

    current_weather = weather_json_obj['properties']['periods'][0]

    weather_report = {
        'shortForecast': current_weather['shortForecast'],
        'temperature': current_weather['temperature'],
        'relativeHumidity': current_weather['relativeHumidity']['value'],
        'windDirection': current_weather['windDirection'],
        'windSpeed': current_weather['windSpeed'],
        'precipitation': current_weather['probabilityOfPrecipitation']['value']
    }

    return weather_report