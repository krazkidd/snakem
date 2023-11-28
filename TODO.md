# TODO.md

- arrange config files to make use of built-in config supported
  https://docs.python.org/3/library/configparser.html

- ignore or add components.d.ts?
  https://github.com/unplugin/unplugin-vue-components#typescript

- DeprecationWarning: the imp module is deprecated in favour of importlib and slated for removal in Python 3.12; see the module's documentation for alternative uses

- fix CORS config (shouldn't allow '*' when deployed)
- server and web url configs need to be hoisted all the way up
  (so we can change during dev and deployment, with envvars or command line args)

- allow server to be FQDN (or "localhost"); need to save resolved IP address; use "localhost" in client config; use "0.0.0.0" as bind address in server config?

  - See: https://docs.python.org/3/library/socket.html

    For IPv4 addresses, two special forms are accepted instead of a host address: '' represents INADDR_ANY, which is used to bind to all interfaces, and the string '<broadcast>' represents INADDR_BROADCAST. This behavior is not compatible with IPv6, therefore, you may want to avoid these if you intend to support IPv6 with your Python programs.

- the game over mode on client needs rework--how do you restart a game? can you even close the game?
  note that the server does not have a game over mode and goes back to the lobby

  - add game over mode which shows stats of previous game

- make it harder to quit running game

- client JOIN message needs some polish; client needs to auto-retry or somethin
  -- or show better messages and show keybinds (e.g. remind player to request to join the game)

- add chat system
  - this can be done in frontend with firebase

- read up on debugging containerized app
  https://docs.docker.com/engine/security/rootless/#install
  https://code.visualstudio.com/docs/containers/debug-common
  https://code.visualstudio.com/docs/containers/reference

- figure out packaging and put this in Dockerfile
  https://docs.python.org/3/distutils/setupscript.html
  https://packaging.python.org/en/latest/

- do we need to watch for desync between the game tick counter and the time elapsed?

  - we changed from static step counter to real timekeeper
  - need to add a prioritization system that drops old net messages or advances game ticks to catch up (e.g. if a game update has been seen, we only want to apply updates from that point)

- use async queue
  https://docs.python.org/3/library/asyncio-queue.html

- review these and make some unit tests for client/server messaging
  \# NOTE: This second example does not work because TestClient manages its own event loop.
  \# See: https://www.starlette.io/testclient/#asynchronous-tests

  \# async def main() -> None:
  \# client = TestClient(app)

  \# response = client.get("/api/health")

  \# assert response.status_code == 200
  \# assert response.json() == {"alive": true, "ready", true}

  \# with client.websocket_connect('/ws') as ws:
  \# await Client(ws, scr, config.STEP_TIME_MS, config.KEYS).start()

  \# async def main() -> None:
  \# async with AsyncClient(app=app, base_url=f'ws://{config.SERVER_HOST}:{config.SERVER_PORT}') as client:
  \# response = await client.get("/api/health")

  \# assert response.status_code == 200
  \# assert response.json() == {"alive": true, "ready", true}
  \# client.send()
  \# #with client.websocket_connect('/ws') as ws:
  \# # await Client(ws, scr, config.STEP_TIME_MS, config.KEYS).start()

- fix server debug launch

- client/server should only sleep long enough to advance the game when in game mode
  - instead of a fixed sleep duration, we need a fixed *step* for more determinism (i.e. we need to account for the time it tacks to update the game state)

- client/server should sync on real time and not just game tick

- client/server should maybe also use game instance ID in case game start/end messages get lost?

  - how does websockets handle lost messages?

- it appears to be possible to join a running game, and late players dont get assigned to a snake; might break something

- add venv as build-time requirement

- install debugpy extension or other remote debug extension to work with container

  - or try vs core remote?

- are these conflicting with each other? the prettier status is read and prettification doesnt seem to be working

  - "devDependencies": {
    "@vue/eslint-config-prettier": "^7.1.0",
    "eslint": "^8.39.0",
    "eslint-plugin-vue": "^9.11.0",
    "prettier": "^2.8.8",
    }

- better config managment

  - python config with environment override at DuckDuckGo
    https://duckduckgo.com/?t=ftsa&q=python+config+with+environment+override&atb=v337-1&ia=web

  - Which is the best way to allow configuration options be overridden at the command line in Python? - Stack Overflow
    https://stackoverflow.com/questions/3609852/which-is-the-best-way-to-allow-configuration-options-be-overridden-at-the-comman

  - bw2/ConfigArgParse: A drop-in replacement for argparse that allows options to also be set via config files and/or environment variables.
    https://github.com/bw2/ConfigArgParse

  - ConfigArgParse · PyPI
    https://pypi.org/project/ConfigArgParse/

  - configparser — Configuration file parser — Python 3.11.3 documentation
    https://docs.python.org/3/library/configparser.html

  - configparser — Configuration file parser — Python 3.11.3 documentation
    https://docs.python.org/3/library/configparser.html#configparser.ConfigParser

  - How to override python configuration with environment variables - Stack Overflow
    https://stackoverflow.com/questions/57178901/how-to-override-python-configuration-with-environment-variables

- should we create a package? we would need one to distribute to PyPi

review these FastAPI docs
- https://github.com/guybedford/es-module-shims#import-maps
- https://fastapi.tiangolo.com/tutorial/response-model/
- https://fastapi.tiangolo.com/advanced/response-directly/
- https://fastapi.tiangolo.com/advanced/additional-responses/
- https://testdriven.io/blog/developing-a-single-page-app-with-fastapi-and-vuejs/
