from server.connection_utils import BoxConnections

# -*- coding: utf-8 -*-
__author__ = 'neo'


# http server url
app_handlers = [
    # websocket_model url, connected by web browser, param = dev_type, dev_code
    (r'/box/(.*)', BoxConnections)
]
