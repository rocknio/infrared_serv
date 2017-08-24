# -*- coding: utf-8 -*-
import json
import logging
import datetime

from models.models import TBoxInfo, TBoxSensor, TTriggerLog
from server.tag_def import TAG_BOX_SERIAL, TAG_SENSOR_TYPE, TAG_SENSOR_ADDR, TAG_TRIGGER_TYPE, TAG_OCCUPIED, \
    TAG_UN_OCCUPIED, TAG_TRANS_ID

__author__ = 'neo'


def get_box_info_by_serial(db, box_serial):
    try:
        box_info = db.query(TBoxInfo).filter(TBoxInfo.box_serial == box_serial).one()
        return box_info
    except Exception as err:
        logging.error("err = {}".format(err))
        return None


def get_box_sensor(db, box_serial, sensor_type, sensor_addr):
    try:
        sensor_info = db.query(TBoxSensor).filter(TBoxSensor.box_serial == box_serial) \
                                          .filter(TBoxSensor.sensor_type == sensor_type) \
                                          .filter(TBoxSensor.sensor_addr == sensor_addr).one()
        return sensor_info
    except Exception as err:
        logging.error("err = {}".format(err))
        return None


def get_occupied_trigger_log(db, box_serial, sensor_type, sensor_addr, transid):
    try:
        occupied_trigger_log = db.query(TTriggerLog).filter(TTriggerLog.box_serial == box_serial) \
                                          .filter(TTriggerLog.sensor_type == sensor_type) \
                                          .filter(TTriggerLog.sensor_addr == sensor_addr) \
                                          .filter(TTriggerLog.transid == transid) \
                                          .filter(TTriggerLog.trigger_type == TAG_OCCUPIED).one()
        return occupied_trigger_log
    except Exception as err:
        logging.error("err = {}".format(err))
        return None


def do_infrared_trigger(db, box_info, sensor_info, infrared_info):
    try:
        if infrared_info[TAG_TRIGGER_TYPE].upper() == TAG_OCCUPIED.upper():
            trigger_log = TTriggerLog()
            trigger_log.box_serial = box_info.box_serial
            trigger_log.sensor_type = sensor_info.sensor_type
            trigger_log.sensor_addr = sensor_info.sensor_addr
            trigger_log.trigger_time = datetime.datetime.now()
            trigger_log.x = sensor_info.x
            trigger_log.y = sensor_info.y
            trigger_log.trigger_type = infrared_info[TAG_TRIGGER_TYPE]
            trigger_log.transid = infrared_info[TAG_TRANS_ID]

            db.add(trigger_log)
            db.commit()
        elif infrared_info[TAG_TRIGGER_TYPE].upper() == TAG_UN_OCCUPIED.upper():
            occupied_trigger_log = get_occupied_trigger_log(db, box_info.box_serial, sensor_info.sensor_type, sensor_info.sensor_addr, infrared_info[TAG_TRANS_ID])
            if occupied_trigger_log is None:
                logging.warning("infrared have not occupied! msg = {}".format(infrared_info))
            else:
                occupied_trigger_log.un_trigger_time = datetime.datetime.now()
                occupied_trigger_log.trigger_type = infrared_info[TAG_TRIGGER_TYPE]
                occupied_trigger_log.duration = (occupied_trigger_log.un_trigger_time - occupied_trigger_log.trigger_time).seconds

                db.add(occupied_trigger_log)
                db.commit()
        else:
            logging.error("invalid trigger type! msg = {}".format(infrared_info))
            return None
    except Exception as err:
        logging.error("err = {}".format(err))
        return None


def infrared_trigger(db, msg):
    try:
        infrared_info = json.loads(msg)
        logging.info("RECV = {}".format(infrared_info))

        box_info = get_box_info_by_serial(db, infrared_info[TAG_BOX_SERIAL])
        if box_info is None:
            logging.error("box serial is invalid, msg = {}".format(infrared_info))
            return None

        sensor_info = get_box_sensor(db, infrared_info[TAG_BOX_SERIAL], infrared_info[TAG_SENSOR_TYPE], infrared_info[TAG_SENSOR_ADDR])
        if sensor_info is None:
            logging.error("box sensor is invalid, msg = {}".format(infrared_info))
            return None

        do_infrared_trigger(db, box_info, sensor_info, infrared_info)
    except Exception as err:
        logging.error("err = {}".format(err))
        return False
