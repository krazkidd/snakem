# TODO

- arrange config files to make use of built-in config supported
  https://docs.python.org/3/library/configparser.html

- fix project structure (i.e. do we need a src folder? how to debug/package/deploy?)

- DeprecationWarning: the imp module is deprecated in favour of importlib and slated for removal in Python 3.12; see the module's documentation for alternative uses

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
  \# assert response.json() == {"status": "alive"}

  \# with client.websocket_connect('/ws') as ws:
  \# await Client(ws, scr, config.STEP_TIME_MS, config.KEYS).start()

  \# async def main() -> None:
  \# async with AsyncClient(app=app, base_url=f'ws://{config.SERVER_HOST}:{config.SERVER_PORT}') as client:
  \# response = await client.get("/api/health")

  \# assert response.status_code == 200
  \# assert response.json() == {"status": "alive"}
  \# client.send()
  \# #with client.websocket_connect('/ws') as ws:
  \# # await Client(ws, scr, config.STEP_TIME_MS, config.KEYS).start()

- fix server debug launch

- client/server should only sleep long enough to advance the game when in game mode

- client/server should sync on real time and not just game tick

- client/server should maybe also use game instance ID in case game start/end messages get lost?

  - how does websockets handle lost messages?

- it appears to be possible to join a running game, and late players dont get assigned to a snake; might break something

- add venv as build-time requirement
