import adsb_tools.aircraft
from pprint import pprint


def get_aircraft(base_url, latitude, longitude):
    aircraft_messages = adsb_tools.aircraft.get_aircraft(base_url, True)
    mapped_aircraft = adsb_tools.aircraft.add_aircraft_options(aircraft_messages, latitude, longitude)

    return mapped_aircraft
