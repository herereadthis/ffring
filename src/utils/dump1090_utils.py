import json
import urllib.request
from adsb_tools.distance.calculate import find_closest
from pprint import pprint




# from typing import List, Dict
import math

EARTH_RADIUS_KM = 6371.0


# def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the great-circle distance between two points on the Earth's surface
    using the Haversine formula.

    Args:
        lat1 (float): Latitude of the first point in degrees
        lon1 (float): Longitude of the first point in degrees
        lat2 (float): Latitude of the second point in degrees
        lon2 (float): Longitude of the second point in degrees

    Returns:
        float: Distance between the two points in kilometers
    """

    # Convert coordinates to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = EARTH_RADIUS_KM * c

    return distance


def get_direction(base_lat, base_lon, dest_lat, dest_lon):
    """Calculate the direction from one coordinate to another."""
    # Calculate the difference between the latitudes and longitudes
    lat_diff = dest_lat - base_lat
    lon_diff = dest_lon - base_lon

    # Calculate the angle between the two points in radians
    angle = math.atan2(lon_diff, lat_diff)

    # Convert the angle from radians to degrees
    degrees = math.degrees(angle)

    # Convert the angle to a compass direction
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    idx = round(degrees / (360.0 / len(directions))) % len(directions)
    direction = directions[idx]

    return degrees, direction


def add_aircraft_options(aircraft_list, base_lat, base_lon):
    """
    Adds additional data to aircraft based on aircraft properties
    """
    aircraft_list_with_options = []
    for aircraft in aircraft_list:
        new_aircraft = aircraft.copy()
        aircraft_lat = new_aircraft['lat']
        aircraft_lon = new_aircraft['lon']

        distance = calculate_distance(base_lat, base_lon, aircraft_lat, aircraft_lon)
        degrees, direction = get_direction(base_lat, base_lon, aircraft_lat, aircraft_lon)

        new_aircraft['distance'] = distance
        new_aircraft['degrees'] = degrees
        new_aircraft['direction'] = direction

        aircraft_list_with_options.append(new_aircraft)

    return sorted(aircraft_list_with_options, key=lambda x: x["distance"])


def get_receiver_options(base_url):
    receiver_url = f'{base_url}/data/receiver.json'

    with urllib.request.urlopen(receiver_url) as response:
        data = response.read().decode()
        json_obj = json.loads(data)

    return {
        'latitude': json_obj['lat'],
        'longitude': json_obj['lon'],
        'refresh': json_obj['refresh'],
        'history': json_obj['history']
    }


def get_aircraft(base_url, latitude, longitude):
    receiver_url = f'{base_url}/data/aircraft.json'
    print(receiver_url)

    with urllib.request.urlopen(receiver_url) as response:
        data = response.read().decode()
        json_obj = json.loads(data)
    
    filtered_aircraft = [
        d for d in json_obj['aircraft']
        if "lat" in d and "lon" in d and d["lat"] is not None and d["lon"] is not None
    ]

    mapped_keys = ['lat', 'lon', 'alt_geom', 'hex', "flight", "category"]
    mapped_aircraft = [{k: v for k, v in d.items() if k in mapped_keys} for d in filtered_aircraft]

    print(f'latitude: {latitude}')    
    print(f'longitude: {longitude}')    
    mapped_aircraft = add_aircraft_options(mapped_aircraft, latitude, longitude)
    pprint(mapped_aircraft[0])

    # closest_dict = find_closest(mapped_aircraft, latitude, longitude)
    # pprint.pprint(closest_dict)