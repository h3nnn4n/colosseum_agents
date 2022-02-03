#!/usr/bin/env python3

import json
import sys

from flask import Flask, request

AGENT_NAME = "dummy"
AGENT_ID = None
app = Flask(__name__)


def agent_logic(state):
    global AGENT_ID

    response = {}

    if state.get("stop"):
        return

    if state.get("set_agent_id"):
        AGENT_ID = state.get("set_agent_id")
        response["agent_name"] = AGENT_NAME

    if state.get("ping"):
        response["pong"] = "boofar"

    if AGENT_ID:
        response["agent_id"] = AGENT_ID

    return response


@app.route("/", methods=["GET"])
def get():
    return "Yes, it works. To communicate with the agent make a POST request."


@app.route("/", methods=["POST"])
def post():
    state = request.json

    actions = agent_logic(state)

    return actions


def main():
    while True:
        data = sys.stdin.readline()
        state = json.loads(data)
        actions = agent_logic(state)

        data_encoded = json.dumps(actions)
        sys.stdout.write(data_encoded + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
