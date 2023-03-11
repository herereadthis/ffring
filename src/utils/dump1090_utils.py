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
    aircraft_messages = aircraft.get_aircraft(base_url, True)
    mapped_aircraft = aircraft.add_aircraft_options(aircraft_messages, latitude, longitude)
    pprint(mapped_aircraft[0])

    return mapped_aircraft
