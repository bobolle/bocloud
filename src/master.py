import uwsgi
import json
import jwt
import time
import os
import sys

sys.path.append(os.path.abspath('src'))
from template import BoTemplate 
from database import *

secret = '44aa99ghghaa'

def master(env, sr):
    path = env['PATH_INFO']
    request = env['REQUEST_METHOD']
    data = env['wsgi.input'].read()

    # GET
    if request == 'GET':
        if path == '/':
            return response(sr, '200 OK', None, 'monitor.html')

        if path == '/monitor':
            # how to know what to query?
            # fetch data
            return response(sr, '200 OK', None, 'monitor.html')
        
        if path == '/api/stream':
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

        if path == '/api/fetch/device':
            device_id = env['QUERY_STRING']
            
            headers = []
            headers.append(('Content-Type', 'application/json'))
            sr('200 OK', headers)

            with Session(engine) as session:
                data = getDeviceReads(session, device_id)
                return json.dumps(data).encode('utf-8')

        # fetch data from sensor
        if path == '/api/fetch/sensor':
            sensor_id = env['QUERY_STRING']

            headers = []
            headers.append(('Content-Type', 'application/json'))
            sr('200 OK', headers)

            with Session(engine) as session:
                data = getSensorReads(session, sensor_id)
                return json.dumps(data).encode('utf-8')

        if path == '/gentoken':
            token = jwt.encode({'user': 'test'}, secret, algorithm="HS256");
            headers = []
            headers.append(('Content-Type', 'application/json'))
            sr('200 OK', headers)
            return json.dumps(token).encode('utf-8')


        if path == '/testtoken':
            auth = env['HTTP_AUTHORIZATION']
            token = auth.split(" ")[1]
            print(jwt.decode(token, secret, algorithms=["HS256"]))

            return response(sr, '200 OK', None, 'base.html')

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
                    device = getDevice(session, device_name)
                    # new device
                    if not device:

                        # new device
                        new_device = createDevice(session, device_name)

                        for sensor_type, value in sensors.items():
                            # create new sensor
                            new_sensor = createSensor(session, sensor_type)
                            # create new read
                            new_read = createRead(session, value)

                            # append read to sensor
                            new_sensor.reads.append(new_read)
                            # append sensor to device
                            new_device.sensors.append(new_sensor)

                            session.add(new_sensor)
                            session.add(new_read)

                        session.add(new_device)
                        session.commit()

                    # device already exists
                    else:
                        for device_sensor in device.sensors:
                            for sensor_type, value in sensors.items():
                                if device_sensor.sensor_type == sensor_type:
                                    # create new read
                                    new_read = createRead(session, value)
                                    # append read to sensor
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
