# -*- coding: utf-8 -*-

import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from settings import DB_CONNECT_STR, is_debug

__author__ = 'Neo'


# 创建对象的基类:
Base = declarative_base()

# 初始化数据库连接:
db_conn_str = DB_CONNECT_STR

# tornado单线程，只需要一个数据库链接即可
engine = create_engine(db_conn_str, pool_recycle=3600, echo=is_debug, isolation_level='READ_UNCOMMITTED')


def check_db():
    """
    检查数据库连接是否可用
    :return:
    """
    try:
        db = scoped_session(sessionmaker(bind=engine))
        db.connection()
        db.remove()
        return True
    except Exception as err:
        logging.fatal("db error = {}".format(err))
        return False
