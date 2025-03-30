import json
import sqlalchemy as db
from sqlalchemy.orm import Session

from models import Device, Sensor, Base

engine = db.create_engine('postgresql+psycopg2://db_user:1234@localhost/db')
Base.metadata.create_all(engine)

def getDevices():
    with Session(engine) as session:
        stmt = session.query(Device).all()
        for device in stmt:
            print(device)
        session.close()
        return stmt

def getSensors():
    with Session(engine) as session:
        stmt = session.query(Sensor).all()
        for sensor in stmt:
            print(sensor)
        session.close()
        return stmt

def getReads():
    with Session(engine) as session:
        stmt = session.query(Read).all()
        for read in stmt:
            print(read)
        session.close()
        return stmt

def createDevice(device_name: str):
    with Session(engine) as session:
        new_device = Device(device_name=device_name)
        session.add(new_device)
        session.commit()

def createSensor(sensor_type: str, device_id: str):
    with Session(engine) as session:
        #get_device = session.query(Device).where(device_id == device_id)
        new_sensor = Sensor(
            sensor_type=sensor_type,
            device_id=device_id
        )
        session.add(new_sensor)
        session.commit()

def createRead(value: str, timestamp: str, sensor_id: str):
    with Session(engine) as session:
        new_read = Read(
            value=value,
            timestamp=timestamp,
            sensor_id=sensor_id
        )
        session.add(new_read)
        session.commit()
