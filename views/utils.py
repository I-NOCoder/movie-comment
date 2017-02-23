from flask import json
from werkzeug.wrappers import Response


class ApiResponse(object):
    def __init__(self, item, status=200):
        self.item = item
        self.status = status

    def response_to(self):
        return Response(json.dumps(self.item),
                        status=self.status,
                        mimetype='application/json')


def success(res=None, status_code=200):
    res = res or {}

    dct = {
        'r': 1
    }

    if res and isinstance(res, dict):
        dct.update(res)

    return ApiResponse(dct, status_code)


def failure(message, status_code):
    dct = {
        'r': 0,
        'status': status_code,
        'message': message
    }

    return dct


def updated(res=None):
    return success(res=res, status_code=200)


def bad_request(message,):
    return failure(message, 400)
