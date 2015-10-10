#-*- encoding: utf-8 -*-
"""封装一些处理请求的方法
"""

from flask import request
import json
import sys

from .response import ApiError
from ..log.logger import logger, Logger

def on_json_loading_failed(e):
    logger.error(Logger.dumps(t='json_load_fail', e=str(e)))
    raise ApiError(400, msg='body is not json')


def get_or_400(dict_data, key):
    """从dict_data中get数据，如果不存在，则返回400"""
    if dict_data is None:
        raise ApiError(400, msg='[%s] does not existed' % key)
    if key not in dict_data:
        raise ApiError(400, msg='[%s] does not existed' % key)
    return dict_data.get(key)

def get_arg_or_400(key):
    """从URL中的某个参数，如果不存在，则返回400"""
    return get_or_400(request.args, key)

def get_int_arg_or_400(key):
    """从URL中的某个整型参数，如果不存在，则返回400"""
    value = get_arg_or_400(key)
    if not value.isdecimal():
        raise ApiError(400, msg='[%s] is not integer' % key)
    return int(value)
