import datetime
import sqlalchemy as db

class Device():
    __tablename__ = "Device"
    device_guid = db.Column(db.Integer, primary_key=True)
    device_type = db.Column(db.String)
    
class Sensor():
    __tablename__ = "Sensor"
    sensor_guid = db.Column(db.Integer, primary_key=True)
    device_guid = db.Column(db.String, db.ForeignKey('Device.device_guid'))

    value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now().time())
