import json
import urllib.request

url = "https://example.com/data.json"


def get_receiver_options(base_url):
    receiver_url = f'{base_url}/data/receiver.json'
    print(receiver_url)

    with urllib.request.urlopen(receiver_url) as response:
        data = response.read().decode()
        json_obj = json.loads(data)

    return {
        'latitude': json_obj['lat'],
        'longitude': json_obj['lon'],
        'refresh': json_obj['refresh'],
        'history': json_obj['history']
    }