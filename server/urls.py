from server.http_serv_utils import InfraredHttpRequestHandler

# -*- coding: utf-8 -*-
__author__ = 'neo'


# http server url
app_handlers = [
    # websocket_model url, connected by web browser, param = dev_type, dev_code
    (r'/', InfraredHttpRequestHandler)
]
