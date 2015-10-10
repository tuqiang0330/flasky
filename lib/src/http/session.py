#-*- encoding: utf-8 -*-
"""使用Memcached存储session，并将sid植入cookie。
session是一个dict，含有user_id
"""

import uuid
import flask

from .response import ApiError, make_api_resp

def set_user_session(user_id):
    session_id = str(uuid.uuid1())
    flask.current_app.config['MEMCACHED'].set(session_id, {'user_id':user_id}, 300)
    resp = make_api_resp()
    resp.set_cookie('sid', session_id)
    return resp

def get_session_or_401():
    session_id = flask.request.cookies.get('sid')
    if session_id is None:
        raise ApiError(status_code=401)
    session = flask.current_app.config['MEMCACHED'].get(session_id)
    if session is None:
        raise ApiError(status_code=401)
    return session

def get_user_id_or_401():
    user_id = get_session_or_401().get('user_id')
    if user_id is None:
        raise ApiError(status_code=401)
    return user_id

def need_session(func):
    """装饰器，使用方式如下：
        @app.route('/get_user_info')
        @need_session
        def get_user_info():
            pass
    """
    def decorator(*args, **kwargs):
        get_session_or_401()
        return func(*args, **kwargs)
    return decorator
