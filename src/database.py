import json
import sqlalchemy as db
from sqlalchemy.orm import Session

from models import Device, Sensor, Read, Base

engine = db.create_engine('postgresql+psycopg2://db_user:1234@localhost/db')
Base.metadata.create_all(engine)

def getDeviceReads(session, device_id: int):
    reads = session.query(Read).join(Sensor).filter(Sensor.device_id == device_id).all()
    if reads:
        data = []
        for read in reads:
            data.append({
                'read_id': read.read_id,
                'value': read.value,
                'timestamp': read.timestamp.isoformat(),
                'sensor_type': read.sensor.sensor_type
                })
    return data

def getDevice(session, device_name: str):
    device = session.query(Device).filter(Device.device_name == device_name).first()
    return device

def createDevice(session, device_name: str):
    new_device = Device(device_name=device_name)
    return new_device

def getSensorReads(session, sensor_id: int):
    reads = session.query(Read).filter(Read.sensor_id == sensor_id).all()
    if reads:
        data = []
        for read in reads:
            data.append({
                'read_id': read.read_id,
                'value': read.value,
                'timestamp': read.timestamp.isoformat()
            })
    return data

def createSensor(session, sensor_type: str):
    new_sensor = Sensor(sensor_type=sensor_type)
    return new_sensor

def createRead(session, value: int):
    new_read = Read(value=value)
    return new_read

def lastReadIndex(session):
    index = session.query(Read).order_by(Read.read_id.desc()).first()
    return index
