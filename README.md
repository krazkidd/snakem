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

### Starting the game:

1. Open a terminal and navigate to the source root folder.
2. Run `$ sudo docker build -t snakem-dev:latest .` to build the Docker image.
3. Run `sudo docker run -d -p 11845:11845/udp --name snakem-dev snakem-dev:latest` to create the Docker container and start the server.
4. Run `sudo docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' snakem-dev` to get the IP address of the container.
5. Update SERVER_HOST in `snakem/config/client.py` with the container IP address.
6. Run `$ python3 -m snakem.net.client` to start the client.

### Debugging the game:

1. Install VS Code and the recommended extensions (see `.vscode/extensions.json`).
2. In the Run and Debug view, launch **snakem server** or **snakem client**.
3. Start the server or client as described in #starting-the-game.
