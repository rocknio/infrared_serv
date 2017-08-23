from server.http_serv_utils import InfraredHttpRequestHandler

# -*- coding: utf-8 -*-
__author__ = 'neo'


# http server url
app_handlers = [
    (r'/innerMap/(.*)', InfraredHttpRequestHandler)
]
