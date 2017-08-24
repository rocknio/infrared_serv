import configparser
import logging

# -*- coding: utf-8 -*-
__author__ = 'neo'


try:
    # parse configure from settings.ini
    config = configparser.ConfigParser()
    config.read('settings.ini')

    LOG_LEVEL = int(config.get('default', 'LOG_LEVEL'))
    SERVER_PORT = int(config.get('default', 'SERVER_PORT'))

    is_debug_str = config.get('default', 'is_debug')
    if is_debug_str.upper() == 'True'.upper():
        is_debug = True
    else:
        is_debug = False

    DB_CONNECT_STR = config.get('default', 'DB_CONNECT_STR')

    POST_RETRY_TIMES = int(config.get('default', 'POST_RETRY_TIMES'))
    POST_REQUEST_TIMEOUT = int(config.get('default', 'POST_REQUEST_TIMEOUT'))
except Exception as e:
    logging.error('parse config fail, error = {}'.format(e))
    exit(0)
