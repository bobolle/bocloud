import uwsgi
import time
import sys
import os

sys.path.append(os.path.abspath('src'))
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
        while True:
            # last read index
            index = env.get('stream-index')

            # create table for connections
            # create custom events
            # device connect
            # device disconnect
            yield b'data: [{"device_id": "pico_w", "data": 30}]\n\n'
            time.sleep(1)
    finally:
        pass
