export enum GameState {
  LOBBY = 0,
  GAME = 1,
}

export enum MsgType {
  MOTD = 0,
  LOBBY_JOIN = 1,
  LOBBY_QUIT = 2,
  READY = 3,
  NOT_READY = 4,
  START = 5,
  SNAKE_UPDATE = 6,
  PELLET_UPDATE = 7,
  CHAT = 8,
  SETUP = 9,
  INPUT = 10,
}

//TODO this is a game enum (not net); should it be moved?
export enum Dir {
  UP = 0,
  DOWN = 1,
  LEFT = 2,
  RIGHT = 3,
}