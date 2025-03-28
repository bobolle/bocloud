import psycopg2
import json
import time
import os
import sys

sys.path.append(os.path.abspath('src'))
from template import BoTemplate 
from database import createDevice  


try:
    conn = psycopg2.connect()
    print('connected to db')
except Exception as e:
    print(e)
#finally:
#    if conn:
#        conn.close()
#        print('db connection closed')


def master(env, sr):
    path = env['PATH_INFO']
    request = env['REQUEST_METHOD']
    data = env['wsgi.input'].read()

    # GET
    if request == 'GET':
        if path == '/':
            try:
                createDevice('01', 'temperature')
            except Exception as e:
                print(e)
            return response(sr, '200 OK', None, 'base.html')

        if path == '/monitor':
            return response(sr, '200 OK', None, 'monitor.html')
        
        if path == '/stream':
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
            return response(sr, '200 OK')

        return response(sr, '404 Not Found', None, 'base.html')

    return response(sr, '404 Not Found', None, 'base.html')

def response(start_response, status_code, headers=None, template_name=None, data=None, body=b''):
    # handle status code, headers, template, data and content
    # working pretty well as it is right now

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
