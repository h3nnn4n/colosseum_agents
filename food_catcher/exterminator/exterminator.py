#!/usr/bin/env python3

import logging

from colosseum_sdk import Agent


AGENT_NAME = "exterminator"


class Exterminator(Agent):
    def __init__(self):
        super(Exterminator, self).__init__(agent_name=AGENT_NAME)

        self.gatherers = set()
        self.killers = set()
        self.targets = {}

    def what_to_spawn_next(self):
        target_gather_kill_ratio = 2
        self.gather_kill_ratio = len(self.gatherers) / (len(self.killers) or 1)

        if self.gather_kill_ratio < target_gather_kill_ratio:
            return "gatherer"
        else:
            return "killer"

    def post_state_update(self):
        actors_alive = set(self.state.actors.mine.ids)
        self.gatherers = self.gatherers & actors_alive
        self.killers = self.killers & actors_alive
        assigned_actors = self.gatherers | self.killers
        idle_actors = self.state.actors.mine.id_not_in(assigned_actors)

        for actor in idle_actors:
            what = self.what_to_spawn_next()
            logging.info(f"added a {what}")
            if what == "killer":
                self.killers.add(actor.id)
            if what == "gatherer":
                self.gatherers.add(actor.id)

        enemies_left = self.state.actors.enemy.count
        enemies_left += self.state.bases.enemy.count
        if enemies_left == 0 and len(self.killers) > 0:
            logging.info(
                f"turning {len(self.killers)} killers into gatherers since there are no enemies left"
            )
            self.gatherers.update(self.killers)
            self.killers.clear()

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
    exterminator = Exterminator()
    logging.info("main")

    while exterminator.run:
        logging.info("loop")
        exterminator.read_state()

        state = exterminator.state
        logging.info(f"{len(state.actors)} {len(state.actors.mine)} {exterminator.gatherers} {exterminator.killers}")
        for actor in state.actors.mine.id_in(exterminator.gatherers):
            food = exterminator.get_food_target_for(actor)

            if actor.distance_to(food) < 0.1:
                logging.info("take food")
                actor.take(food)
            elif actor.food > 100:
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

        if len(exterminator.killers) >= 1:
            logging.info("kill mode")
            base = state.bases.mine.first
            enemy = state.actors.enemy.closest_to(base) or state.bases.enemy.closest_to(
                base
            )

            for actor in state.actors.mine.id_in(exterminator.killers):
                if not enemy:
                    break

                if actor.distance_to(enemy) < 4:
                    actor.attack(enemy)
                else:
                    actor.move(enemy)

        for base in state.bases.mine:
            if base.food > 100 and state.actors.mine.count < 6:
                closest_actor = state.actors.mine.closest_to(base)
                if base.distance_to(closest_actor) > 3:
                    base.spawn()

        exterminator.send_commands()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception(e)
