import functools
import json

from flask import jsonify


def return_json(func):
    """
    A decorator function that converts the output of a function into a JSON response.
    """
    @functools.wraps(func)
    def inner(**kwargs):
        response = jsonify(func(**kwargs))
        response.data = json.dumps(response.json, separators=(',', ':'))
        response.content_type = 'application/json'

        return response

    return inner
