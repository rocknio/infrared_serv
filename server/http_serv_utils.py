# -*- coding: utf-8 -*-
__author__ = 'neo'

import tornado.web
import logging


class InfraredHttpRequestHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(InfraredHttpRequestHandler, self).__init__(application, request, **kwargs)
        self._linkid = id(self)

    def data_received(self, chunk):
        pass

    def get_linkid(self):
        return self._linkid

    def on_finish(self):
        logging.info("This link[%d] finished" % self._linkid)
