def master(env, sr):
    path = env['PATH_INFO']
    bpath = path.encode('utf-8')

    sr('200 OK', [('Content-Type', 'text/html')])
    return [b"hello dawg"]
