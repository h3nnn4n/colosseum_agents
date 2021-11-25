#!/usr/bin/env python3.10

import logging
from random import random

from colosseum_sdk import Agent


AGENT_NAME = "half_rusher"


def main():
    agent = Agent(agent_name=AGENT_NAME)

    rush = random() < 0.5

    while agent.run:
        agent.read_state()

        state = agent.state

        base = state.bases.mine.first
        enemy = state.actors.enemy.closest_to(base) or state.bases.enemy.closest_to(
            base
        )

        if enemy and rush:
            for actor in state.actors.mine:
                if actor.distance_to(enemy) < 4:
                    actor.attack(enemy)
                else:
                    actor.move(enemy)
        else:
            for actor in state.actors.mine:
                food = state.foods.closest_to(actor)

                if actor.distance_to(food) < 0.1:
                    actor.take(food)
                elif actor.food > 100:
                    base = state.bases.closest_to(actor)
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
