import uwsgi
import json
import time
import os
import sys

sys.path.append(os.path.abspath('src'))
from template import BoTemplate 
from database import *

def master(env, sr):
    path = env['PATH_INFO']
    request = env['REQUEST_METHOD']
    data = env['wsgi.input'].read()

    # GET
    if request == 'GET':
        if path == '/':
            return response(sr, '200 OK', None, 'base.html')

        if path == '/monitor':
            # how to know what to query?
            # fetch data
            return response(sr, '200 OK', None, 'monitor.html')
        
        if path == '/stream':
            # get index of last read
            with Session(engine) as session:
                index = lastReadIndex(session)

            # send as a headers
            if index:
                uwsgi.add_var('stream-index', bytes(f'{index.read_id}', 'utf-8'))
            else:
                uwsgi.add_var('stream-index', b'0')

            # will be routed to offload
            headers = [('Content-Type', 'text/event-stream')]
            sr('200 OK', headers)

            return b''

        return response(sr, '404 Not Found', None, 'base.html')

    # PUT 
    if request == 'PUT':
        return response(sr, '404 Not Found', None, 'base.html')

    # POST
    if request == 'POST':
        if path == '/api/data':
            json_data = json.loads(data.decode())

            # {
            # "device_id": "pico_w_test",
            # "sensors": {
            #     "moist": 37,
            #     "light": 368
            # }
            #}

            try: 
                device_name = json_data['device_id']
                sensors = json_data['sensors']

                with Session(engine) as session:
                    if not getDevice(session, device_name):
                        new_device = createDevice(session, device_name)

                        for sensor, value in sensors.items():
                            new_sensor = createSensor(session, sensor)
                            new_read = createRead(session, value)

                            new_device.sensors.append(new_sensor)
                            new_sensor.reads.append(new_read)

                            session.add(new_sensor)
                            session.add(new_read)

                        session.add(new_device)
                        session.commit()

                    else:
                        device = getDevice(session, device_name)
                        for device_sensor in device.sensors:
                            for sensor, value in sensors.items():
                                if device_sensor.sensor_type == sensor:
                                    new_read = createRead(session, value)
                                    device_sensor.reads.append(new_read)
                                    session.add(new_read)

                        session.commit()

            except Exception as e:
                print(e)

            return response(sr, '200 OK')

        return response(sr, '404 Not Found', None, 'base.html')

    return response(sr, '404 Not Found', None, 'base.html')

def response(start_response, status_code, headers=None, template_name=None, data=None, body=b''):
    if headers is None:
        headers = [('Content-Type', 'text/html')]

    template = None
    if template_name:
        templateHandler = BoTemplate(template_name)
        templateHandler.parse()
        if data:
            templateHandler.add_data(data)

        template = templateHandler.get()
        headers.append(('Content-Length', str(len(template))))
        start_response(status_code, headers)

        return [template]

    else:
        headers.append(('Content-Length', str(len(body))))
        start_response(status_code, headers)
        return [body]
