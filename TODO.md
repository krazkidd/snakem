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
