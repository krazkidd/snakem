import curses
import curses.ascii

# the address of the main server to connect to
SERVER_HOST: str = '127.0.0.1'
SERVER_PORT: int = 11845

# how fast to advance the game state
STEP_TIME_MS: int = 100

############ KEY BINDINGS ############

KEYS_LOBBY_QUIT: list[int] = [curses.ascii.ESC, ]
KEYS_LOBBY_REFRESH: list[int] = [ord('X'), ord('x'), ]
KEYS_LOBBY_READY: list[int] = [ord('R'), ord('r'), ]
#KEYS_LOBBY_1PLAYER: list[int] = [ord('Y'), ord('y'), ]

KEYS_GAME_QUIT = [curses.ascii.ESC, ]

KEYS_MV_UP: list[int] = [ord('W'), ord('w'), ord('K'), ord('k',), curses.KEY_UP, ]
KEYS_MV_LEFT: list[int] = [ord('A'), ord('a'), ord('H'), ord('h'), curses.KEY_LEFT, ]
KEYS_MV_DOWN: list[int] = [ord('S'), ord('s'), ord('J'), ord('j',), curses.KEY_DOWN, ]
KEYS_MV_RIGHT: list[int] = [ord('D'), ord('d'), ord('L'), ord('l',), curses.KEY_RIGHT, ]
