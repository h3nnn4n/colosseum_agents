#!/usr/bin/env python3

from colosseum_sdk import Agent

AGENT_NAME = "bot_do_coloquio"


def main():
    agent = Agent(agent_name=AGENT_NAME)

    while agent.run:
        agent.read_state()
        state = agent.state

        for actor in state.actors.mine:
            food = state.foods.closest_to(actor)

            if actor.distance_to(food) < 0.1:
                actor.take(food)
            elif actor.food > 500:
                base = state.bases.mine.closest_to(actor)
                if actor.distance_to(base) >= 0.1:
                    actor.move(base)
                else:
                    actor.deposit_food(base)
            else:
                actor.move(food)

        for base in state.bases.mine:
            if base.food > 100 and state.actors.mine.count < 1:
                base.spawn()

        agent.send_commands()


if __name__ == "__main__":
    main()
