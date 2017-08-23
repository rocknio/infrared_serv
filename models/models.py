# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Float, Index, Integer, SmallInteger, String, Table
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

    id = Column(Integer, primary_key=True)
    box_serial = Column(String(32), nullable=False, index=True)
    sensor_type = Column(String(32))
    sensor_name = Column(String(32))
    sensor_addr = Column(SmallInteger)
    min_value = Column(Float(asdecimal=True))
    max_value = Column(Float(asdecimal=True))


class TBoxWarnning(Base):
    __tablename__ = 't_box_warnning'
    __table_args__ = (
        Index('idx_box_warnning_bdt', 'box_serial', 'sensor_addr', 'sensor_type'),
        Index('idx_box_warnning_box_sensor_type', 'box_serial', 'sensor_type')
    )

    id = Column(Integer, primary_key=True)
    box_serial = Column(String(32), nullable=False, index=True)
    sensor_addr = Column(SmallInteger)
    sensor_type = Column(String(32), nullable=False)
    warnning_type = Column(String(16), nullable=False)
    value = Column(Float(asdecimal=True))
    status = Column(Integer)
    warnning_time = Column(DateTime)
    recover_time = Column(DateTime)


class TDeviceData(Base):
    __tablename__ = 't_device_data'

    id = Column(BigInteger, primary_key=True)
    box_serial = Column(String(32), index=True)
    transid = Column(String(32), index=True)
    dev_type = Column(String(32))
    dev_addr = Column(SmallInteger)
    dev_value = Column(Float(asdecimal=True))
    timestamp = Column(DateTime)


class TOperator(Base):
    __tablename__ = 't_operator'

    id = Column(Integer, primary_key=True)
    account = Column(String(32))
    name = Column(String(64))
    password = Column(String(32))
    mobile = Column(String(16))
    email = Column(String(32))
    roleId = Column(String(32))
    status = Column(Integer)
    createAccount = Column(String(32))
    createTime = Column(DateTime)
    box_serial = Column(String(255))


t_t_role_perm = Table(
    't_role_perm', metadata,
    Column('roleId', Integer),
    Column('permId', String(255))
)


class TStatusDict(Base):
    __tablename__ = 't_status_dict'
    __table_args__ = (
        Index('idx_status_dict_status', 'table_name', 'status'),
    )

    id = Column(Integer, primary_key=True)
    table_name = Column(String(32), nullable=False)
    status = Column(Integer, nullable=False)
    status_desc = Column(String(64), nullable=False)


class TSysconfig(Base):
    __tablename__ = 't_sysconfig'

    id = Column(Integer, primary_key=True)
    paraname = Column(String(32))
    paradesc = Column(String(32))
    value = Column(String(128))
    minval = Column(Integer)
    maxval = Column(Integer)
    paratype = Column(Integer)
    displaymode = Column(String(8))
    classid = Column(Integer)
    opdate = Column(DateTime)
