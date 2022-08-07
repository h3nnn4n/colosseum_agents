#!/usr/bin/env python3

from utils import send_commands, get_state, get_internal_id, distance
import logging
from random import choice


AGENT_NAME = "manhattan"
AGENT_ID = None


logging.basicConfig(
    filename=f"{AGENT_NAME}_{get_internal_id()}.log", level=logging.INFO
)


def update(state):
    logging.info(state)
    foods = state.get("foods")
    if foods is None:
        logging.info("food not found")
        return

    snake = state.get("snakes", {}).get(AGENT_ID)
    if snake is None:
        logging.info("snake info not found")
        return

    if not snake.get("alive"):
        logging.info("ded snek")
        return

    snake_position = snake.get("head_position")
    nearest_food = foods[0]
    nearest_food_distance = float("inf")

    for food in foods:
        dist = distance(snake_position, food)
        if dist < nearest_food_distance:
            dist = nearest_food_distance
            nearest_food = food

    logging.info(f"{food=} {snake_position=}")

    if nearest_food[0] < snake_position[0]:
        return "LEFT"
    if nearest_food[0] > snake_position[0]:
        return "RIGHT"

    if nearest_food[1] < snake_position[1]:
        return "UP"
    if nearest_food[1] > snake_position[1]:
        return "DOWN"

    logging.info("random move")
    return choice(["UP", "RIGHT", "DOWN", "LEFT"])


def main():
    global AGENT_ID

    while True:
        state = get_state()
        response = {}

        if state.get("stop"):
            break

        if state.get("set_agent_id"):
            AGENT_ID = state.get("set_agent_id")
            response["agent_name"] = AGENT_NAME

        if state.get("ping"):
            response["pong"] = "boofar"

        if AGENT_ID:
            response["agent_id"] = AGENT_ID

        next_move = update(state)
        if next_move:
            response["move"] = next_move

        send_commands(response)


if __name__ == "__main__":
    main()
