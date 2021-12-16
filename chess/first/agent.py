#!/usr/bin/env python3

import logging

import chess

from utils import get_internal_id, get_state, send_commands

AGENT_NAME = "first"


logging.basicConfig(
    filename=f"{AGENT_NAME}_{get_internal_id()}.log", level=logging.INFO
)


def agent_logic(state):
    epd = state.get("epd")
    if not epd:
        logging.debug("got no board state")
        return

    board = chess.Board()
    board.set_epd(epd)
    legal_moves = board.legal_moves
    move = list(legal_moves)[0].__str__()
    logging.debug(f"picking {move} out of {list(legal_moves)}")
    logging.info(f"playing {move}")

    return move


def main():
    agent_id = None

    while True:
        state = get_state()
        response = {}

        if state.get("stop"):
            break

        if state.get("set_agent_id"):
            agent_id = state.get("set_agent_id")
            response["agent_name"] = AGENT_NAME

        if state.get("ping"):
            response["pong"] = "boofar"

        if agent_id:
            response["agent_id"] = agent_id

        move = agent_logic(state)
        if move:
            response["move"] = move

        send_commands(response)


if __name__ == "__main__":
    main()
