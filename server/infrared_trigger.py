# -*- coding: utf-8 -*-
import json
import logging

__author__ = 'neo'


def get_box_info_by_serial(db, serial):
    try:
        db.
    except Exception as err:
        logging.error("err = {}".format(err))
        return False


def infrared_trigger(db, msg):
    try:
        infrared_info = json.loads(msg)

    except Exception as err:
        logging.error("err = {}".format(err))
        return False
