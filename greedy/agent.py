#!/usr/bin/env python3.10

import logging

from colosseum_sdk import Agent


AGENT_NAME = "greedy"


def main():
    agent = Agent(agent_name=AGENT_NAME)

    while agent.run:
        agent.read_state()
        state = agent.state

        for actor in state.actors.mine:
            food = state.foods.closest_to(actor)

            if actor.distance_to(food) < 0.1:
                actor.take(food)
            elif actor.food > 200:
                base = state.bases.mine.closest_to(actor)
                if actor.distance_to(base) >= 0.1:
                    actor.move(base)
                else:
                    actor.deposit_food(base)
            else:
                actor.move(food)

        agent.send_commands()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception(e)
