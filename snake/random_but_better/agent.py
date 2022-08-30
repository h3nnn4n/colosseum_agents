#!/usr/bin/env python3

from utils import send_commands, get_state, get_internal_id
import logging
from random import choice


AGENT_NAME = "random_but_better"
AGENT_ID = None


logging.basicConfig(
    filename=f"{AGENT_NAME}_{get_internal_id()}.log", level=logging.INFO
)


def _build_grid(state):
    grid_width = state["grid"]["width"]
    grid_height = state["grid"]["height"]

    base_grid = []
    for _ in range(grid_width):
        row = []
        for _ in range(grid_height):
            row.append(False)

        base_grid.append(row)

    for agent_id, snake in state["snakes"].items():
        logging.info(snake)

        if not snake["alive"]:
            continue

        for x, y in snake["positions"]:
            base_grid[x][y] = True

    return base_grid


def get_non_suicidal_move(snake_position, grid):
    snake_x, snake_y = snake_position

    grid_width = len(grid)
    grid_height = len(grid[0])

    if snake_x > 0 and not grid[snake_x - 1][snake_y]:
        return "LEFT"
    if snake_x < grid_width - 1 and not grid[snake_x + 1][snake_y]:
        return "RIGHT"

    if snake_y > 0 and not grid[snake_x][snake_y - 1]:
        return "UP"
    if snake_y < grid_height - 1 and not grid[snake_x][snake_y + 1]:
        return "DOWN"

    logging.info(f"non suicidal move not found {snake_position=} RIP")

    return None


def get_random_move():
    return choice(["UP", "RIGHT", "DOWN", "LEFT"])


def update(state):
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

    grid = _build_grid(state)

    non_suicidal_move = get_non_suicidal_move(snake_position, grid)
    random_move = get_random_move()

    return non_suicidal_move or random_move


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

        try:
            next_move = update(state)
        except Exception as e:
            logging.exception(e)
            next_move = get_random_move()

        if next_move:
            response["move"] = next_move

        send_commands(response)


if __name__ == "__main__":
    main()
