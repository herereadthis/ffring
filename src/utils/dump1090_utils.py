import json
import urllib.request
from adsb_tools.distance.calculate import find_closest
import pprint

url = "https://example.com/data.json"


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

    # Define a mapping of keys to their new names
    key_map = {'lat': 'latitude', 'lon': 'longitude', 'alt_geom': 'altitude'}

    # Use dictionary comprehension and map to create a new list of dictionaries
    mapped_aircraft = [{
        key_map.get(k, k): v for k, v in d.items() if k in key_map or k in ['hex', 'flight', 'category']
    } for d in filtered_aircraft]


    # for d in mapped_aircraft:

    #     d['z'] = d['x'] * d['y']
    
    pprint.pprint(mapped_aircraft)

    closest_dict = find_closest(mapped_aircraft, latitude, longitude)
    pprint.pprint(closest_dict)