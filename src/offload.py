import uwsgi
import time
import sys
import os

sys.path.append(os.path.abspath('src'))
from sqlalchemy import event
from database import *

def stream(env, sr):
    headers = []
    headers.append(('Content-Type','text/event-stream'))
    headers.append(('Cache-Control','no-cache'))
    headers.append(('Connection','keep-alive'))
    sr('200 OK', headers)

    # trying to yield to closed socket will make uwsgi throw an OSError: write error
    # nothing to worry about if we exit from this instance


    try:
        # last read index
        index = env.get('stream-index')
        with Session(engine) as session:
            while True:
                # starting with getting every read
                new_read = session.query(Read).filter(Read.read_id > index).first()
                if new_read:
                    #print(f'data: {{"device": "{new_read.sensor.device.device_name}","sensor": "{new_read.sensor.sensor_type}","value": {new_read.value}}}')
                    yield(bytes(f'data: {{"device": "{new_read.sensor.device.device_name}","sensor": "{new_read.sensor.sensor_type}","value": {new_read.value}}}\n\n', 'utf-8'))
                    index = new_read.read_id
                    new_read = None
                else:
                    time.sleep(1)
                    continue

    finally:
        pass
