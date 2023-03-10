import json
import requests
from adsb_tools import aircraft
from pprint import pprint


def get_receiver_options(base_url):
    receiver_url = f'{base_url}/data/receiver.json'
    
    response = requests.get(receiver_url)
    json_obj = json.loads(response.content)
    print('retrieved reciever response.')

    return json_obj


def get_aircraft(base_url, latitude, longitude):
    receiver_url = f'{base_url}/data/aircraft.json'

    response = requests.get(receiver_url)
    json_obj = json.loads(response.content)
    print('retrieved aircraft response.')

    filtered_aircraft = [
        d for d in json_obj['aircraft']
        if "lat" in d and "lon" in d and d["lat"] is not None and d["lon"] is not None
    ]

    mapped_keys = ['lat', 'lon', 'alt_geom', 'hex', "flight", "category", "gs", "true_heading"]
    mapped_aircraft = [{k: v for k, v in d.items() if k in mapped_keys} for d in filtered_aircraft]

    print(f'latitude: {latitude}')    
    print(f'longitude: {longitude}')    
    mapped_aircraft = aircraft.add_aircraft_options(mapped_aircraft, latitude, longitude)
    pprint(mapped_aircraft[0])

    return mapped_aircraft
