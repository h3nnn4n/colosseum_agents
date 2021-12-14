#!/usr/bin/env python3.10

import logging

from colosseum_sdk import Agent


AGENT_NAME = "greedy_replicator"


def main():
    agent = Agent(agent_name=AGENT_NAME)

    while agent.run:
        agent.read_state()
        state = agent.state
        main_base = state.bases.mine.first

        for actor in state.actors.mine:
            food = state.foods.closest_to(actor)

            if actor.distance_to(food) < 0.1:
                actor.take(food)
            elif actor.food > 250:
                base = state.bases.mine.closest_to(actor)
                if actor.distance_to(base) >= 0.1:
                    actor.move(base)
                else:
                    actor.deposit_food(base)
            else:
                actor.move(food)

        if main_base and main_base.can_spawn and state.actors.mine.count < 2:
            base.spawn()

        agent.send_commands()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception(e)
