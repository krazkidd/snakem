import curses
import curses.ascii

# the address of the main server to connect to
SERVER_HOST: str = '127.0.0.1'
SERVER_PORT: int = 9000

KEYS: dict = {
    'LOBBY_QUIT': [curses.ascii.ESC, ],
    'LOBBY_REFRESH': [ord('X'), ord('x'), ],
    'LOBBY_READY': [ord('R'), ord('r'), ],
    #'LOBBY_1PLAYER': [ord('Y'), ord('y'), ],

    'GAME_QUIT': [curses.ascii.ESC, ],

    'MV_UP': [ord('W'), ord('w'), ord('K'), ord('k',), curses.KEY_UP, ],
    'MV_LEFT': [ord('A'), ord('a'), ord('H'), ord('h'), curses.KEY_LEFT, ],
    'MV_DOWN': [ord('S'), ord('s'), ord('J'), ord('j',), curses.KEY_DOWN, ],
    'MV_RIGHT': [ord('D'), ord('d'), ord('L'), ord('l',), curses.KEY_RIGHT, ],
}
