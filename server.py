import json
import time
import os

# lazy temp file for storing data from session
temp_json_data = []
temp_json_data_counter = 0

def master(env, sr):
    global temp_json_data_counter
    path = env['PATH_INFO']
    request = env['REQUEST_METHOD']
    data = env['wsgi.input'].read()

    #print(env)
    #print(data)
    
    # GET
    if request == 'GET':
        if path == '/':
            return response(sr, '200 OK', None, 'base.html', b'index/home')

        if path == '/temp':
            return response(sr, '200 OK', None, 'table.html', json.dumps(temp_json_data).encode('utf-8'))
        
        if path == '/stream':
            headers = [('Content-Type', 'text/event-stream')]
            headers.append(('Cache-Control', 'no-cache'))
            headers.append(('Connection', 'keep-alive'))

            sr('200 OK', headers)

            return b'data: [{"test": 30}, {"dd": "asdf", "ff": 13}]\n\n'

        else:
            return response(sr, '404 Not Found', None, 'base.html', b'404 Not Found')

    # PUT 
    if request == 'PUT':
        return response(sr, '404 Not Found', None, 'base.html', b'404 Not Found')

    # POST
    if request == 'POST':
        if path == '/api/data':
            json_data = json.loads(data.decode())
            temp_json_data.append(json_data)
            temp_json_data_counter += 1
            return response(sr, '200 OK')

        else:
            return response(sr, '404 Not Found', None, 'base.html', b'404 Not Found')

    return response(sr, '404 Not Found', None, 'base.html', b'404 Not Found')

def response(start_response, status_code, headers=None, template_name=None, body=b''):
    template = None

    if headers is None:
        headers = [('Content-Type', 'text/html')]

    if template_name:
        template_path = os.path.join('template', template_name)

        try:
            with open(template_path, 'r') as template_file:
                template = template_file.read()
        except FileNotFoundError:
            start_response('404 Not Found', [('Content-Type', 'text/plain')])
            return [b'Template not found.']

    start_response(status_code, headers)

    if template:
        if body:
            body_content = body.decode('utf-8')
            if '<bodycontent>' in template:
                template = template.replace('<bodycontent>', f'<body>{body_content}</body>')

        if template_name == 'table.html':
            if '<jsondata>' in template:
                table_data = ''
                if temp_json_data:
                    for d in temp_json_data:
                        table_data += '<tr><td>device</td><td>test</td><tr>'
                    template = template.replace('<jsondata>', table_data)

        headers.append(('Content-Length', str(len(template))))
        return [template.encode('utf-8')]

    else:
        headers.append(('Content-Length', str(len(body))))
        return [body]
