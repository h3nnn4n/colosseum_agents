#!/usr/bin/env python3

import json
import sys
from random import choice

AGENT_NAME = "random"


def main():
    agent_id = None
    while True:
        data = sys.stdin.readline()
        state = json.loads(data)
        response = {}

        if state.get("stop"):
            break

        if state.get("set_agent_id"):
            agent_id = state.get("set_agent_id")
            response["agent_name"] = AGENT_NAME

        if state.get("ping"):
            response["pong"] = "boofar"

        if agent_id:
            response["agent_id"] = agent_id

        response["move"] = choice(["UP", "RIGHT", "DOWN", "LEFT"])

        send_commands(response)


def send_commands(data):
    data_encoded = json.dumps(data)
    sys.stdout.write(data_encoded + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
