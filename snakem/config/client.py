import curses
import curses.ascii

# the address of the main server to connect to
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 11845

# how often to advance the game state
STEP_TIME = 0.1

############ KEY BINDINGS ############

KEYS_LOBBY_QUIT = (curses.ascii.ESC, )
KEYS_LOBBY_REFRESH = (ord('X'), ord('x'), )
KEYS_LOBBY_READY = (ord('R'), ord('r'), )
#KEYS_LOBBY_1PLAYER = (ord('Y'), ord('y'), )

KEYS_GAME_QUIT = (curses.ascii.ESC, )

KEYS_MV_UP = (ord('W'), ord('w'), ord('K'), ord('k',), curses.KEY_UP, )
KEYS_MV_LEFT = (ord('A'), ord('a'), ord('H'), ord('h'), curses.KEY_LEFT, )
KEYS_MV_DOWN = (ord('S'), ord('s'), ord('J'), ord('j',), curses.KEY_DOWN, )
KEYS_MV_RIGHT = (ord('D'), ord('d'), ord('L'), ord('l',), curses.KEY_RIGHT, )

################ DEBUG ###############

PRINT_DEBUG = True
PRINT_ERROR = True
PRINT_NETMSG = False
