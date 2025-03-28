import json
import sqlalchemy as db

from models import Device, Sensor

engine = db.create_engine('postgresql+psycopg2://db_user:1234@localhost/db')

def createDevice(device_guid: int, device_type: str) -> bool:
    db.insert(Device).values(device_guid = device_guid, device_type = device_type)
    return True
