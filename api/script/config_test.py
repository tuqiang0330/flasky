DEBUG = True

import logging
LOG_LEVEL = logging.DEBUG
LOG_FILE = '/home/flasky/api/log'

SQLALCHEMY_DATABASE_URI = 'mysql://flasky:flasky@localhost/flasky'
SQLALCHEMY_ECHO = True

from werkzeug.contrib.cache import MemcachedCache
MEMCACHED = MemcachedCache(['127.0.0.1:11211'], default_timeout=3600*24*90, key_prefix='flasky')
