#!/usr/bin/env python3.10

import logging

from colosseum_sdk import Agent

AGENT_NAME = "botzera"


class Botzera(Agent):
    def __init__(self):
        super(Botzera, self).__init__(agent_name=AGENT_NAME)

        self.gatherers = set()
        self.targets = {}

    def post_state_update(self):
        actors_alive = set(self.state.actors.mine.ids)
        self.gatherers = self.gatherers & actors_alive
        assigned_actors = self.gatherers
        idle_actors = self.state.actors.id_not_in(assigned_actors)

        for actor in idle_actors:
            self.gatherers.add(actor.id)

    def _valid_food(self, food):
        food_id = food.id
        for f in self.state.foods:
            if food_id == f.id:
                return True
        return False

    def _get_free_food_for(self, actor):
        used_ids = [f.id for f in self.targets.values()]
        return self.state.foods.id_not_in(used_ids).closest_to(actor)

    def get_food_target_for(self, actor):
        if actor.id not in self.targets.keys():
            self.targets[actor.id] = self._get_free_food_for(actor)
        elif not self._valid_food(self.targets[actor.id]):
            self.targets[actor.id] = self._get_free_food_for(actor)

        if not self.targets[actor.id]:
            self.targets[actor.id] = self.state.foods.random

        return self.targets[actor.id]


def main():
    agent = Botzera()
    logging.info("main")

    while agent.run:
        logging.debug("loop")
        agent.read_state()

        state = agent.state
        logging.info(f"{len(state.actors.mine)} {len(state.actors.mine)}")
        for actor in state.actors.mine.id_in(agent.gatherers):
            food = agent.get_food_target_for(actor)

            if actor.distance_to(food) < 0.1:
                logging.info("take food")
                actor.take(food)
            elif actor.food > 200:
                base = state.bases.mine.closest_to(actor)
                if actor.distance_to(base) >= 0.1:
                    logging.info("move to base")
                    actor.move(base)
                else:
                    logging.info("deposit_food")
                    actor.deposit_food(base)
            else:
                logging.info("move to food")
                actor.move(food)

        base = state.bases.mine.first
        if base and base.food > 100 and state.actors.count < 2:
            closest_actor = state.actors.mine.closest_to(base)
            if base.distance_to(closest_actor) > 3:
                base.spawn()

        agent.send_commands()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception(e)
