from django.http import HttpResponse
import os
import json


def is_dir(path):
    return os.path.isdir(path)

def is_file(path):
    return os.path.isfile(path)

def json_response(data={}):
    return HttpResponse(json.dumps(data))


class PayloadParser:

    _data = {}

    def __init__(self, body):
        self._data = json.loads(body)

    def get(self, field, default=None):
        return self._data.get(field, default)
