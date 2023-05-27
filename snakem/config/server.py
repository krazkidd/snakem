# the address the main server binds to
BIND_ADDR: str = ''
# port = 0 will use random port
BIND_PORT_HEALTH_CHECK: int = 11844
BIND_PORT: int = 11845

# welcome message for new clients
MOTD: str = 'Welcome to my Snake-M development server!'

############# GAME SETUP #############

# game dimensions (units are text cells)
WIN_WIDTH: int = 60
WIN_HEIGHT: int = 35

# how fast to advance the game state
STEP_TIME_MS: int = 100
