# -*- coding: utf-8 -*-
from server.deal_request import deal_get_path, deal_get_heat
from server.infrared_trigger import infrared_trigger
import logging
import tornado.web
from sqlalchemy.orm import scoped_session, sessionmaker
from server.dbutils import engine
from server.tag_def import TAG_METHOD_GET_HEAT, TAG_METHOD_GET_PATH, TAG_METHOD_INFRARED_TRIGGER

__author__ = 'neo'


class InfraredHttpRequestHandler(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(InfraredHttpRequestHandler, self).__init__(application, request, **kwargs)
        self._linkid = id(self)
        self._db = scoped_session(sessionmaker(bind=engine))

    def data_received(self, chunk):
        pass

    def get_linkid(self):
        return self._linkid

    def on_finish(self):
        self._db.remove()
        logging.info("This link[%d] finished" % self._linkid)

    def get(self, method):
        try:
            req = self.request.body()
            if str(method).upper() == TAG_METHOD_GET_PATH.upper():
                deal_get_path(req)
            elif str(method).upper() == TAG_METHOD_GET_HEAT.upper():
                deal_get_heat(req)
            elif str(method).upper() == TAG_METHOD_INFRARED_TRIGGER.upper():
                infrared_trigger(req)
            else:
                self.set_status(501)
                self.write("method invalid, method = {}".format(method))
        except Exception as err:
            logging.error("Internal failed! err = {}".format(err))
            self.set_status(500)
            self.write("Internal failed! err = {}".format(err))
