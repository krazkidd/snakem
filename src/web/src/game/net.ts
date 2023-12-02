import type { UseWebSocketReturn } from '@vueuse/core';

import { Dir, GameState, MsgType } from './enums';

export interface Message {
    _msg_type: MsgType,
    [key: string]: any;
}

export interface MotdMessage extends Message {
    _msg_type: MsgType.MOTD,
    motd: string,
}

export interface QuitMessage extends Message {
    _msg_type: MsgType.LOBBY_QUIT,
}

export interface PelletUpdateMessage extends Message {
    _msg_type: MsgType.PELLET_UPDATE,
    tick: number,
    pellet_id: number,
    pos_x: number,
    pos_y: number,
}

export interface SnakeUpdateMessage extends Message {
    _msg_type: MsgType.SNAKE_UPDATE,
    tick: number,
    snake_id: number,
    heading: Dir,
    is_alive: boolean,
    //TODO might have to use arrays (rather than tuples) for body piece positions
    body: [number, number][],
}

export interface LobbyJoinRequestMessage extends Message {
    _msg_type: MsgType.LOBBY_JOIN,
}

export interface ReadyMessage extends Message {
    _msg_type: MsgType.READY,
}

export interface StartMessage extends Message {
    _msg_type: MsgType.START,
    width: number,
    height: number,
    step_time_ms: number,
}

export interface InputMessage extends Message {
    _msg_type: MsgType.INPUT,
    tick: number,
    heading: Dir,
}

// how long to wait for a network message or other input event
export const TIMEOUT = 0.005;

export function sendMessage<T extends Message>(ws: WebSocket | UseWebSocketReturn<T>, msgType: MsgType, data: Record<string, any> | null = null) {
    if (!data) {
        data = { _msg_type: msgType };
    } else {
        data['_msg_type'] = msgType
    }

    if (ws instanceof WebSocket) {
        return ws.send(JSON.stringify(data));
    } else {
        return ws.send(JSON.stringify(data));
    }
}
