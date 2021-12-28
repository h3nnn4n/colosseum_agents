#!/usr/bin/env python3.10

import logging

from colosseum_sdk import Agent

AGENT_NAME = "nearest_pick_greedy"


def get_internal_id():
    import random
    import string
    from datetime import datetime

    now = datetime.now()

    random_string = "".join(
        random.choices(
            string.ascii_lowercase + string.ascii_uppercase + string.digits, k=6
        )
    )
    return "_".join([now.strftime("%y%m%d%H%M%S"), random_string])


def main():
    logging.basicConfig(
        filename=f"{AGENT_NAME}_{get_internal_id()}.log", level=logging.INFO
    )

    agent = Agent(agent_name=AGENT_NAME)
    logging.info("main")

    while agent.run:
        logging.debug("loop")
        agent.read_state()

        state = agent.state
        logging.info(f"{len(state.actors)} {len(state.actors)}")
        for actor in state.actors:
            food = state.foods.closest_to(actor)

            if actor.distance_to(food) < 0.1:
                logging.info("take food")
                actor.take(food)
            elif actor.food > 250:
                base = state.bases.closest_to(actor)
                if actor.distance_to(base) >= 0.1:
                    logging.info("move to base")
                    actor.move(base)
                else:
                    logging.info("deposit_food")
                    actor.deposit_food(base)
            else:
                logging.info("move to food")
                actor.move(food)

        for base in state.bases:
            if base.food > 100 and state.actors.count < 1:
                base.spawn()

        agent.send_commands()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception(e)
