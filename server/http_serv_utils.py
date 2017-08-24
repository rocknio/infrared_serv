# -*- coding: utf-8 -*-
import logging

import tornado.web
from sqlalchemy.orm import scoped_session, sessionmaker

from server.dbutils import engine
from server.deal_request import deal_get_path, deal_get_heat
from server.infrared_trigger import infrared_trigger
from server.tag_def import TAG_METHOD_GET_HEAT, TAG_METHOD_GET_PATH

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
            if str(method).upper() == TAG_METHOD_GET_PATH.upper():
                res = deal_get_path()
            elif str(method).upper() == TAG_METHOD_GET_HEAT.upper():
                res = deal_get_heat()
            else:
                self.set_status(501)
                self.write("method invalid, method = {}".format(method))
                return

            if res:
                self.write(res)
        except Exception as err:
            logging.error("Internal failed! err = {}".format(err))
            self.set_status(500)
            self.write("Internal failed! err = {}".format(err))

    def post(self):
        """
        {
            "box_serial": "11111",
            "sensor_type": "infrared",
            "sensor_addr": 1,
            "trigger_type": "Occupied",
            "transid": "transid"
        }
        :return:
        """
        try:
            infrared_trigger(self._db, self.request.body())
        except Exception as err:
            logging.error("Internal failed! err = {}".format(err))
            self.set_status(500)
            self.write("Internal failed! err = {}".format(err))
