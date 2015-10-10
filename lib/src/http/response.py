#-*- encoding: utf-8 -*-

import uuid
from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def get_status_msg(status_code):
    """将status code转换为status message
        200 => 'OK'
        400 => 'Bad Request'
        500 => 'Internal Server Error'
    """
    return HTTP_STATUS_CODES.get(status_code, 'Unknown Error')

def make_api_resp(data={}, status_code=200, msg='OK'):
    data.update({'status_code':status_code, 'msg':msg, 'request_id':str(uuid.uuid1())})
    resp = jsonify(data)
    resp.status_code = status_code
    return resp


class ApiError(Exception):
    def __init__(self, status_code, data={}, msg=None):
        if msg is None:
            msg = get_status_msg(status_code)
        self.status_code = status_code
        self.data = data
        self.data.update({'status_code':status_code, 'msg':msg, 'request_id':str(uuid.uuid1())})


def api_error_handler(api_error):
    """需要在注册到app的error_handler中

        @app.error_handler(repsonse.ApiError)
        def api_error_handler(api_error)
            return response.api_error_handler(api_error)

    """
    resp = jsonify(api_error.data)
    resp.status_code = api_error.status_code
    return resp
