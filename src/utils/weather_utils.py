import json
import requests
from pprint import pprint
import pytz
from datetime import datetime, timezone

def get_current_event(events):
    """
    Given a list of events that have start time and end time, return the event
    that matches the interval for the current time.
    """
    current_time = datetime.now(timezone.utc)

    for event in events:
        start_time = event['startTime']
        end_time = event['endTime']
        if isinstance(start_time, str):
            start_time = datetime.fromisoformat(start_time)
        if isinstance(end_time, str):
            end_time = datetime.fromisoformat(end_time)
        if start_time.tzinfo is None:
            start_time = start_time.replace(tzinfo=timezone.utc)
        if end_time.tzinfo is None:
            end_time = end_time.replace(tzinfo=timezone.utc)
        if start_time <= current_time <= end_time:
            return event

    return None


def get_localized_time(date_time, local_timezone, date_time_format = "%-I:%M%p"):
    """
    takes a datetime object and returns a human-readable local time
    """
    formatted_time = datetime.fromisoformat(date_time)
    local_time = formatted_time.astimezone(local_timezone)
    local_formatted_time = local_time.strftime(date_time_format)
    return local_formatted_time


def get_weather_data(latitude, longitude):
    """
    Get the current weather data from a specified URL and return as a dictionary
    """
    grid_url = f'https://api.weather.gov/points/{latitude},{longitude}'
    grid_response = requests.get(grid_url)
    grid_json_obj = json.loads(grid_response.content)

    grid_properties =  grid_json_obj['properties']
    grid_timezone =  grid_properties['timeZone']
    local_timezone = pytz.timezone(grid_timezone)
    forcast_hourly_url = grid_properties['forecastHourly']
    weather_response = requests.get(forcast_hourly_url)
    weather_json_obj = json.loads(weather_response.content)

    current_weather = get_current_event(weather_json_obj['properties']['periods'])

    local_formatted_start_time = get_localized_time(current_weather['startTime'], local_timezone)
    local_formatted_end_time = get_localized_time(current_weather['endTime'], local_timezone)

    weather_report = {
        'startTime': local_formatted_start_time,
        'endTime': local_formatted_end_time,
        'shortForecast': current_weather['shortForecast'],
        'temperature': current_weather['temperature'],
        'relativeHumidity': current_weather['relativeHumidity']['value'],
        'windDirection': current_weather['windDirection'],
        'windSpeed': current_weather['windSpeed'],
        'precipitation': current_weather['probabilityOfPrecipitation']['value'],
        'period': current_weather,
        'local_timezone': local_timezone,
        'grid_url': grid_url,
        'forcast_hourly_url': forcast_hourly_url
    }

    return weather_report
