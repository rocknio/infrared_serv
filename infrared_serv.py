import logging
import logging.handlers
import os
import sys
import threading

import tornado.httpserver
from tornado.ioloop import IOLoop

from server.dbutils import check_db
from server.infrared_utils import read_serial
from server.urls import app_handlers
from settings import SERVER_PORT, LOG_LEVEL

# -*- coding: utf-8 -*-
__author__ = 'neo'


def init_logging():
    """
    init logging module
    """
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)

    sh = logging.StreamHandler()
    file_log = logging.handlers.TimedRotatingFileHandler('infrared_serv.log', 'MIDNIGHT', 1, 0)
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)-7s] [%(filename)s-%(funcName)s-%(lineno)d] %(message)s')
    sh.setFormatter(formatter)
    file_log.setFormatter(formatter)

    logger.addHandler(sh)
    logger.addHandler(file_log)

    logging.info("Current log level is : %s", logging.getLevelName(logger.getEffectiveLevel()))


def check_python_version():
    if sys.version[:1] != '3':
        return False
    else:
        return True


def log_process_info():
    p_pid, pid = None, None
    if hasattr(os, 'getppid'):  # only available on Unix
        p_pid = os.getppid()
    pid = os.getpid()

    logging.info("Monitor Server: {},{}".format(pid, p_pid))


def hide_win32_console():
    try:
        import platform
        if platform.system() == 'Windows' or platform.system() == 'windows':
            # hide console window
            import ctypes
            whnd = ctypes.windll.kernel32.GetConsoleWindow()
            if whnd != 0:
                ctypes.windll.user32.ShowWindow(whnd, 0)
                ctypes.windll.kernel32.CloseHandle(whnd)
    except Exception:
        pass


def start_http_serv():
    try:
        # server configurations
        app = tornado.web.Application(
            handlers=app_handlers
        )

        api_server = tornado.httpserver.HTTPServer(app, xheaders=True)
        api_server.listen(SERVER_PORT)
        logging.info("Start server at: %d", SERVER_PORT)

        # start event loop
        IOLoop.instance().start()
    except Exception as err:
        logging.fatal('Infrared HTTP Server start fail! err = %s' % err)


def start_receive_serial_data():
    try:
        read_serial()
    except Exception as err:
        logging.fatal('Infrared HTTP Server start fail! err = %s' % err)


if __name__ == "__main__":
    try:
        if check_python_version() is False:
            print('Please use python3 run the program')
            exit()

        init_logging()

        if check_db() is False:
            exit()

        hide_win32_console()

        log_process_info()

        t_http = threading.Thread(target=start_http_serv)
        t_serial = threading.Thread(target=start_receive_serial_data)

        t_http.start()
        t_serial.start()
    except Exception as e:
        log_str = 'Infrared Server start fail! err = %s' % e
        logging.fatal(log_str)
