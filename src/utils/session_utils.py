import os
import datetime as dt
from sys import platform
import json
import requests
import sys
import toml


ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..'))


def get_config():
    """ get file path of the config file """
    config_file_path = os.path.join(ROOT_DIR, 'config.toml')

    try:
        assert (os.path.isfile(config_file_path)), 'config.toml file missing!'
    except Exception as err:
        print(err)
        sys.exit()

    return toml.load(config_file_path)
