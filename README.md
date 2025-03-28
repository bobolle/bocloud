# BoCloud

Lazy uwsgi based cloud for managing iot-hub, storing data and make analyses.

The goal is to create a lightweight cloud I can use for my other projects and to learn more about the architecture of a cloud.

### working but not finished functionality:
- handle requests and responses
- routing
- templates
- interface manipulation such as drag and resize
- stream data over sse

### future functionality:
- control panel for device handling
- status panel
- db storage (start with in memory database?)
- sessions

### TODO:
- [x] working connection from fog
- [ ] implement docker-compsose config with postgresql
- [ ] handle connections
- [ ] send back commands to fog
- [x] move js to seperate file
- [ ] refactor everything lol
- [x] option for creating new table per device
- [x] resize tables

## start
```
./master
./offload
```

![](https://i.imgur.com/TXxBmFx.png)
