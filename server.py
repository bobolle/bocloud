import json

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
            return response(sr, '200 OK', None, b'index')

        if path == '/temp':
            return response(sr, '200 OK', [('Content-Type', 'application/json'), ('Refresh', '5')], json.dumps(temp_json_data).encode('utf-8'))

        else:
            return response(sr, '404 Not Found', None, b'404 Not Found')

    # PUT 
    if request == 'PUT':
        return response(sr, '404 Not Found', None, b'404 Not Found')

    # POST
    if request == 'POST':
        if path == '/api/data':
            json_data = json.loads(data.decode())
            temp_json_data.append(json_data)
            return response(sr, '200 OK')

        else:
            return response(sr, '404 Not Found', None, b'404 Not Found')

    return response(sr, '404 Not Found', None, b'404 Not Found')

def response(start_response, status_code, headers=None, body=b''):
    if headers is None:
        headers = [('Content-Type', 'text/plain')]
    headers.append(('Content-Length', str(len(body))))
    start_response(status_code, headers)
    return [body]
