# BoCloud

Lazy uwsgi based cloud for managing iot-hub, storing data and make analyses.

### Solution for streaming data

How I solved requests being blocked when trying to stream over sse was to offload the sse request to another uwsgi instance. So when the master instance returns a response with a text/event-stream header it routes that request to the offload instance. That way the master instance can continue handling request without being blocked by the sse stream.

### Data persistence

Storing data happends on the /api/data POST request where the json data gets stored in the postgesql database.

### /Monitor view

The main idea was to let the user decide how the interface would look like. From that idea I created a template with some table elements that you can resize and move however you like. The size and position get stored in localStorage and set on refresh.

### Goals

The goal is to create a lightweight cloud I can use for my other projects and to learn more about the architecture of a cloud.

### working but not finished functionality:
- handle requests and responses
- routing
- templates
- monitoring view
- non-blocking offload for streaming over sse
- interface manipulation such as drag and resize
- db storage (postgresql)

### TODO:
- [x] working connection from fog
- [ ] implement docker-compsose config with postgresql
- [ ] handle connections
- [ ] send back commands to fog
- [x] move js to seperate file
- [ ] refactor everything lol
- [x] option for creating new table per device
- [x] resize tables
- [ ] control panel for device handling
- [ ] when clicking on a device, add new panel to show reads from that device
- [ ] add close button on panels
- [ ] status panel
- [ ] sessions
- [ ] show previous reads before session in stream panel?

## start
```
./master
./offload
```

![](https://i.imgur.com/TXxBmFx.png)
