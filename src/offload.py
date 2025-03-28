import time

def sse(env, sr):
    headers = []
    headers.append(('Content-Type','text/event-stream'))
    headers.append(('Cache-Control','no-cache'))
    sr('200 OK', headers)

    while True:
        time.sleep(1)
        yield b'data: [{"device_id": "pico_w", "data": 30}]\n\n'
