#!/usr/bin/env python3.10

import logging

from colosseum_sdk import Agent


AGENT_NAME = "base_agent_wrapper"


def main():
    agent = Agent(agent_name=AGENT_NAME)

    while agent.run:
        agent.read_state()
        agent.send_commands()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception(e)
