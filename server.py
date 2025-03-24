import json
import os

# lazy temp file for storing data from session
temp_json_data = [];

def master(env, sr):
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
        #body_content = body.decode('utf-8')
        #if '<body>' in template and '</body>' in template:
        #    template = template.replace('<body>', f'<body>{body_content}')
        if template_name == 'table.html':
            if '<jsondata>' in template:
                table_data = ''
                for d in temp_json_data:
                    table_data += '<tr><td>device</td><td>test</td><tr>'
                template = template.replace('<jsondata>', table_data)

        headers.append(('Content-Length', str(len(template))))
        return [template.encode('utf-8')]

    else:
        headers.append(('Content-Length', str(len(body))))
        return [body]
