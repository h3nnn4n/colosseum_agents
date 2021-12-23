#!/usr/bin/env python3

# The chess code was taken from https://github.com/AnthonyASanchez/python-chess-ai

import logging

import chess

from utils import get_internal_id, get_state, send_commands

AGENT_NAME = "alpha_beta_prunner"


logging.basicConfig(
    filename=f"{AGENT_NAME}_{get_internal_id()}.log", level=logging.INFO
)


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


def agent_logic(state):
    epd = state.get("epd")
    if not epd:
        logging.debug("got no board state")
        return

    board = chess.Board()
    board.set_epd(epd)

    move = minimaxRoot(4, board, True)
    move = move.uci()

    logging.info(f"playing {move}")

    return move


def minimaxRoot(depth, board, isMaximizing):
    possibleMoves = board.legal_moves
    bestMove = -9999
    bestMoveFinal = None

    for x in possibleMoves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        value = max(
            bestMove, minimax(depth - 1, board, -10000, 10000, not isMaximizing)
        )
        board.pop()
        if value > bestMove:
            bestMove = value
            bestMoveFinal = move

    return bestMoveFinal


def minimax(depth, board, alpha, beta, is_maximizing):
    if depth == 0:
        return -evaluation(board)
    possibleMoves = board.legal_moves
    if is_maximizing:
        bestMove = -9999
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            bestMove = max(
                bestMove, minimax(depth - 1, board, alpha, beta, not is_maximizing)
            )
            board.pop()
            alpha = max(alpha, bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove
    else:
        bestMove = 9999
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            bestMove = min(
                bestMove, minimax(depth - 1, board, alpha, beta, not is_maximizing)
            )
            board.pop()
            beta = min(beta, bestMove)
            if beta <= alpha:
                return bestMove
        return bestMove


def calculateMove(board):
    possible_moves = board.legal_moves

    bestMove = None
    bestValue = -9999
    n = 0

    for x in possible_moves:
        move = chess.Move.from_uci(str(x))
        board.push(move)
        boardValue = -evaluation(board)
        board.pop()
        if boardValue > bestValue:
            bestValue = boardValue
            bestMove = move

    return bestMove


def evaluation(board):
    i = 0
    evaluation = 0
    x = True

    try:
        x = bool(board.piece_at(i).color)
    except AttributeError as e:
        x = x

    while i < 63:
        i += 1
        evaluation = evaluation + (
            getPieceValue(str(board.piece_at(i)))
            if x
            else -getPieceValue(str(board.piece_at(i)))
        )

    return evaluation


def getPieceValue(piece):
    if piece is None:
        return 0

    value = 0
    if piece == "P" or piece == "p":
        value = 10
    if piece == "N" or piece == "n":
        value = 30
    if piece == "B" or piece == "b":
        value = 30
    if piece == "R" or piece == "r":
        value = 50
    if piece == "Q" or piece == "q":
        value = 90
    if piece == "K" or piece == "k":
        value = 900

    return value


if __name__ == "__main__":
    main()
