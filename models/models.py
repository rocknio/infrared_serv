# coding: utf-8
from sqlalchemy import Column, DateTime, Float, Index, Integer, SmallInteger, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class TBoxInfo(Base):
    __tablename__ = 't_box_info'

    id = Column(Integer, primary_key=True)
    account = Column(String(32))
    box_serial = Column(String(32), nullable=False, index=True)
    name = Column(String(32))
    addr = Column(String(256))


class TBoxSensor(Base):
    __tablename__ = 't_box_sensor'
    __table_args__ = (
        Index('idx_bos_sensor_sta', 'box_serial', 'sensor_type', 'sensor_addr'),
    )

    id = Column(Integer, primary_key=True)
    box_serial = Column(String(32), nullable=False, index=True)
    sensor_type = Column(String(32))
    sensor_name = Column(String(32))
    sensor_addr = Column(SmallInteger)
    min_value = Column(Float(asdecimal=True))
    max_value = Column(Float(asdecimal=True))
    x = Column(Integer)
    y = Column(Integer)


class TTriggerLog(Base):
    __tablename__ = 't_trigger_log'

    id = Column(Integer, primary_key=True)
    box_serial = Column(String(32))
    sensor_type = Column(String(32))
    sensor_addr = Column(SmallInteger)
    trigger_time = Column(DateTime)
    un_trigger_time = Column(DateTime)
    duration = Column(Integer)
