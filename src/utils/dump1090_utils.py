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
    # pprint(mapped_aircraft[0])

    return mapped_aircraft

def get_aircraft_image(aircraft_hex):
    headers = {
        'User-Agent': 'My Unique User Agent'
    }
    planespotter_url = f'https://api.planespotters.net/pub/photos/hex/{aircraft_hex}'
    response = requests.get(planespotter_url, headers=headers)
    json_obj = json.loads(response.content)

    image = {}
    if (json_obj['photos'] and json_obj['photos'][0] and bool(json_obj['photos'][0])):
        photo_attributes = json_obj['photos'][0]
        thumbnail = photo_attributes['thumbnail']
        thumbnail_large = photo_attributes['thumbnail_large']
        target_photo = thumbnail if thumbnail_large is None else thumbnail_large
        image = {
            'height': target_photo['size']['height'],
            'width': target_photo['size']['width'],
            'src': target_photo['src'],
            'url': planespotter_url
        }
    
    return image

