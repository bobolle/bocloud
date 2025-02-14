def master(env, sr):
    path = env['PATH_INFO']
    request = env['REQUEST_METHOD']
    data = env['wsgi.input'].read()

    #print(env)
    #print(data)

    # GET
    if request == 'GET':
        return response(sr, '200 OK')

    # PUT 
    if request == 'PUT':
        return response(sr, '200 OK')

    # POST
    if request == 'POST':
        return response(sr, '200 OK')

    return response(sr, '404 Not Found')

def response(start_response, status_code, headers=None, body=b''):
    if headers is None:
        headers = [('Content-Type', 'text/plain')]
    headers.append(('Content-Length', str(len(body))))
    start_response(status_code, headers)
    return [body]
