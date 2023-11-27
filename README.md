# Snake-M

Thanks for playing my snake game! This project doesn't have a real
name, so for the purposes of copyright and what-not, I'll just call it
Snake-M (M for Multiplayer).

Author: Mark Ross

Contact: krazkidd@gmail.com

Project hosted at: https://github.com/krazkidd/snakem

License: GPLv3 (see LICENSE.md file)

### Features:

- ...

### Requires:

- POSIX OS (terminal with curses support is required)
- Python 3.11 or later
- Docker CLI

### Starting the server (local):

1. Open a terminal and navigate to the source root folder.
2. Run `$ python3 -m venv .venv` to create the virtual Python environment.
3. Run `$ source .venv/bin/activate` to enter the virtual environment.
4. Run `$ pip install -r requirements.txt` to install all dependencies in the virtual environment.
5. Run `$ uvicorn snakem.web.app:app --host 127.0.0.1 --port 9000 --log-level debug --reload` to start the server.

### Starting the server (Docker):

1. Open a terminal and navigate to the source root folder.
2. Run `$ sudo docker build -t snakem-dev:latest .` to build the Docker image.
3. Run `$ sudo docker run -d -p 9000:9000/tcp --name snakem-dev snakem-dev:latest` to create the Docker container and start the server.
4. Run `$ sudo docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' snakem-dev` to get the IP address of the container.
5. Update SERVER_HOST in `snakem/config/client.py` with the container IP address.

### Starting the client:

1. Run `$ python3 -m snakem.net.client` to start the client.

### Starting the web app:

1. Run `$ npm run dev` to start the web app in dev mode.

### Debugging:

1. Install VS Code and the recommended extensions (see `.vscode/extensions.json`).
2. In the Run and Debug view, launch **snakem server** or **snakem client**.

### Deploy your own server:

[![Deploy to DO](https://www.deploytodo.com/do-btn-blue.svg)](https://cloud.digitalocean.com/apps/new?repo=https://github.com/krazkidd/snakem/tree/master&refcode=b9ac212b7d29)
