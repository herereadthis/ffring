from adsb_tools import aircraft
from pprint import pprint


def get_aircraft(base_url, latitude, longitude):
    aircraft_messages = aircraft.get_aircraft(base_url, True)
    mapped_aircraft = aircraft.add_aircraft_options(aircraft_messages, latitude, longitude)
    # pprint(mapped_aircraft[0])

    return mapped_aircraft

