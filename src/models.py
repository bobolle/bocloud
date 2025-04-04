import datetime
from typing import List
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Device(Base):
    __tablename__ = "Device"

    device_id: Mapped[int] = mapped_column(primary_key=True)
    device_name: Mapped[str]
    sensors: Mapped[List["Sensor"]] = relationship(
            back_populates="device", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Device(device_id={self.device_id!r}, device_name={self.device_name!r})"
    
class Sensor(Base):
    __tablename__ = "Sensor"

    sensor_id: Mapped[int] = mapped_column(primary_key=True)
    sensor_type: Mapped[str]

    device_id: Mapped[int] = mapped_column(ForeignKey('Device.device_id'))
    device : Mapped["Device"] = relationship(back_populates="sensors")

    reads: Mapped[List["Read"]] = relationship(back_populates="sensor", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Sensor(sensor_id={self.sensor_id!r}, sensor_type={self.sensor_type!r}, device={self.device!r})"

class Read(Base):
    __tablename__ = "Read"

    read_id = Column(Integer, primary_key=True)
    value = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.now())

    sensor_id = Column(Integer, ForeignKey('Sensor.sensor_id'))
    sensor: Mapped["Sensor"] = relationship(back_populates="reads")

    def __repr__(self) -> str:
        return f"Read(read_id={self.read_id!r}, value={self.value!r}, timestamp={self.timestamp!r}, sensor={self.sensor!r})"
