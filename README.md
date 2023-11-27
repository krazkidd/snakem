# Snake-M

Play snake with your friends!

<!-- [Try the live app now!](https://krazkidd.github.io/snakem/) -->

Project hosted at: https://github.com/krazkidd/snakem

License: GPLv3 (see LICENSE.md file)

## Features

- ...

## Development

This is a monorepo with three components:

* Game server (Python)
* Game client (Python)
* Web frontend (Vue.js)

The game server and client are packaged together as a Python module. Uvicorn (with FastAPI) is the web server, providing a WebSockets endpoint for game client communications and a RESTful API for the web frontend.

### Starting the server (local)

1. Open a terminal and navigate to `src/server/`.
2. Run `$ python3 -m venv .venv` to create the virtual Python environment.
3. Run `$ source .venv/bin/activate` to enter the virtual environment.
4. Run `$ pip install -r requirements.txt` to install all dependencies in the virtual environment.
5. Run `$ uvicorn snakem.web.app:app --host 127.0.0.1 --port 9000 --log-level debug --reload` to start the server.

### Starting the server (Docker)

1. Open a terminal and navigate to `src/server/`.
2. Run `$ sudo docker build -t snakem:latest .` to build the Docker image.
3. Run `$ sudo docker run -d -p 9000:9000/tcp --name snakem snakem:latest` to create the Docker container and start the server.

To get the container IP address:

1. Run `$ sudo docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' snakem`.

### Starting the client

1. Open a terminal and navigate to `src/server/`.
2. Update `SERVER_HOST` in `snakem/config/client.py` with the server IP address as needed.
3. Run `$ python3 -m snakem.net.client` to start the client.

### Starting the web app

1. Open a terminal and navigate to `src/web/`.
2. Update `__SERVER_URL__` in `vite.config.js` with the server IP address as needed.
3. Run `$ npm run dev` to start the web app.

### Debugging

1. Install VS Code and the recommended extensions (see `.vscode/extensions.json`).
2. In the Run and Debug view, launch **snakem server** or **snakem client**.

### Deploy your own server

[![Deploy to DO](https://www.deploytodo.com/do-btn-blue.svg)](https://cloud.digitalocean.com/apps/new?repo=https://github.com/krazkidd/snakem/tree/master&refcode=b9ac212b7d29)
