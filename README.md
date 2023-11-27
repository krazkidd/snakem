# Snake-M

Play snake with your friends!

<!-- [Try the live app now!](https://krazkidd.github.io/snakem/) -->

Project hosted at: https://github.com/krazkidd/snakem

License: GPLv3 (see LICENSE.md file)

## Features

- ...

## Development

This is a monorepo with three components:

* Game server

  _Requires:_

  * Python ^3.11 or Docker CLI

* Game client

  _Requires:_

  * Python ^3.11
  * POSIX OS (terminal with curses support)

* Web frontend

  _Requires:_

  * A modern browser supported by Vue.js

The game server and client are packaged together as a Python module. Uvicorn (with FastAPI integration) is the web server, providing a WebSockets endpoint for game client communications and a RESTful API for the web frontend.

### Starting the server (local)

It is customary to utilize Python's virtualization facilities to avoid dependency conflicts.

1. To create and enter a virtual Python environment, run

    ```ShellSession
    $ cd src/server
    $ python3 -m venv .venv
    $ source .venv/bin/activate
    ```

2. To install all dependencies in the virtual environment, run

    ```ShellSession
    $ pip install -r requirements.txt
    ```

    From here, you are able to run the Snake-M client or server.

3. To exit the virtual environment, run

    ```ShellSession
    $ deactivate
    ```

---

To start the server from the Python virtual environment, run

```ShellSession
$ uvicorn snakem.web.app:app --host 127.0.0.1 --port 9000 --log-level debug --reload
```

### Starting the server (container)

To build and run the server in a Docker container, run

```ShellSession
$ cd src/server
$ sudo docker build -t snakem:latest .
$ sudo docker run --rm -it -p 9000:9000/tcp --name snakem snakem:latest
```

To get the container IP address and port, run

```ShellSession
$ sudo docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' snakem
```

### Starting the client:

First ensure `SERVER_HOST` in `src/server/snakem/config/client.py` has the right server IP address and port.

To start the client, run

```ShellSession
$ cd src/server
$ python3 -m snakem.net.client
```

### Starting the web app

First ensure `__SERVER_URL__` in `src/web/vite.config.js` has the right server IP address.

```ShellSession
$ cd src/web
$ npm run dev
```

### Debugging (VS Code)

1. Install the recommended extensions (see `.vscode/extensions.json`).

2. Open the Command Palette and execute `python.setInterpreter`. Select the interpreter installed in the virtual environment location (`src/server/.venv/bin/python`).

3. In the Run and Debug view, launch either
   - **snakem server (local)**
   - **snakem client (local)**

### Deploy your own (DigitalOcean)

This repository provides a configuration template for DigitalOcean's App Platform. You can launch your own Snake-M server in the cloud in a couple of clicks with the button below.

[![Deploy to DO](https://www.deploytodo.com/do-btn-blue.svg)](https://cloud.digitalocean.com/apps/new?repo=https://github.com/krazkidd/snakem/tree/master&refcode=b9ac212b7d29)
