# the address the main server binds to
BIND_ADDR = '127.0.0.1'
BIND_PORT = 11845

# welcome message for new clients
MOTD = 'Welcome to my Snake-M development server!'

############# GAME SETUP #############

# game dimensions (units are text cells)
WIN_WIDTH, WIN_HEIGHT = 60, 35

# how often to advance the game state
STEP_TIME = 0.1

################ DEBUG ###############

PRINT_DEBUG = True
PRINT_ERROR = True
PRINT_NETMSG = True
