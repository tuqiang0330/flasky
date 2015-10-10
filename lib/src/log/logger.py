#-*- encoding: utf-8 -*-
"""简单的logging封装，做了以下设定：
1. 一个工程只使用同一个log name
2. 只有DEBUG级别才输出到StreamHandler
3. 使用TimedRotatingFileHandler存储到本地，以天为单位分隔，保留30天

使用方式：
1. 初始化(必须先初始化)
    log.Logger.init_logger(logging.INFO, '/path/to/log/file')
2. 获取logger对象
    log = logger.logger
    或者
    log = logger.Logger.get_logger()
3. 记录日志
    log.info('new request')
    log.error(Logger.dumps(t='error', msg='unknown error'))
"""

import logging, logging.handlers
import json

class Logger:
    log_name = 'flasky'
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(thread)d - %(message)s')

    @staticmethod
    def init_logger(level, file_name, when='D', interval=1, backupCount=30):
        logger = logging.getLogger(Logger.log_name)
        logger.setLevel(level)

        file_handler = logging.handlers.TimedRotatingFileHandler(file_name, when=when, interval=interval, backupCount=backupCount)
        file_handler.setFormatter(Logger.formatter)
        logger.addHandler(file_handler)

        if level <= logging.DEBUG:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(Logger.formatter)
            logger.addHandler(stream_handler)

    @staticmethod
    def get_logger():
        return logger

    @staticmethod
    def dumps(**kwargs):
        """将参数转换成为JSON字符串"""
        return json.dumps(kwargs, ensure_ascii=False)

logger = logging.getLogger(Logger.log_name)
