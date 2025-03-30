import json
import sqlalchemy as db
from sqlalchemy.orm import Session

from models import Device, Sensor, Read, Base

engine = db.create_engine('postgresql+psycopg2://db_user:1234@localhost/db')
Base.metadata.create_all(engine)

def getDevice(session, device_name: str):
        device = session.query(Device).filter(Device.device_name == device_name).first()
        return device

def createDevice(session, device_name: str):
    new_device = Device(device_name=device_name)
    return new_device

def createSensor(session, sensor_type: str):
    new_sensor = Sensor(sensor_type=sensor_type)
    return new_sensor

def createRead(session, value: int):
    new_read = Read(value=value)
    return new_read
