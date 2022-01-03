#!/usr/bin/env python3.10

import json
import logging
import random
import string
import sys
from datetime import datetime
from enum import Enum, auto, unique

AGENT_NAME = "master_exploder"
AGENT_ID = None


@unique
class FailureModes(Enum):
    CRASH_ON_STARTUP = auto()
    CRASH_MIDWAY = auto()
    NO_PING = auto()
    EMPTY_PING = auto()
    DONT_SET_AGENT_NAME = auto()
    INCORRECT_AGENT_ID = auto()
    NONE_AGENT_ID = auto()
    INVALID_JSON_PAYLOAD = auto()

    # TODO:
    # try acting on someone elses entities
    # send invalid actions
    # CHANGE_AGENT_ID = auto()


def main():
    global AGENT_ID

    logging.basicConfig(
        filename=f"{AGENT_NAME}_{get_internal_id()}.log", level=logging.INFO
    )

    failure_mode = random.choice(list(FailureModes))

    logging.info(f"{failure_mode=}")

    while True:
        state = get_state()
        response = {}

        # TODO: Add timeout failure here
        # TODO: Break here
        if state.get("stop"):
            logging.info(f"stopping, reason: {state.get('stop')}")
            break

        if state.get("set_agent_id"):
            if failure_mode == FailureModes.CRASH_ON_STARTUP:
                logging.info("crashing on startup")
                raise RuntimeError("Boom!")

            logging.info(f"{AGENT_ID=}")
            AGENT_ID = state.get("set_agent_id")
            if failure_mode == FailureModes.NONE_AGENT_ID:
                logging.info("setting agent id to none")
                AGENT_ID = None
            elif failure_mode == FailureModes.INCORRECT_AGENT_ID:
                logging.info("setting incorrect agent id")
                AGENT_ID = "boom"

            if failure_mode != FailureModes.DONT_SET_AGENT_NAME:
                response["agent_name"] = AGENT_NAME
            else:
                logging.info("not setting agent name")

        if state.get("ping"):
            logging.info("got ping")
            if failure_mode == FailureModes.NO_PING:
                logging.info("not replying to ping")
            elif failure_mode == FailureModes.EMPTY_PING:
                response["pong"] = None
                logging.info("replying to ping with None")
            else:
                logging.info("replying to ping as normal")
                response["pong"] = "foobar"

        if len(state.get("actors", [])) > 0:
            if failure_mode == FailureModes.CRASH_MIDWAY:
                logging.info("crashing midway")
                raise RuntimeError("Boom!")

        if AGENT_ID:
            response["agent_id"] = AGENT_ID

        if failure_mode == FailureModes.INVALID_JSON_PAYLOAD:
            data = "".join(
                random.choices(
                    string.ascii_lowercase + string.ascii_uppercase + string.digits,
                    k=10,
                )
            ) + "\n"
            sys.stdout.write(data)
            sys.stdout.flush()
        else:
            send_commands(response)


def get_state():
    logging.debug("waiting for data")
    data = sys.stdin.readline()
    logging.debug(f"got data: {data}")
    state = json.loads(data)
    return state


def send_commands(data):
    data_encoded = json.dumps(data)
    sys.stdout.write(data_encoded + "\n")
    sys.stdout.flush()


def get_internal_id():
    now = datetime.now()

    random_string = "".join(
        random.choices(
            string.ascii_lowercase + string.ascii_uppercase + string.digits, k=6
        )
    )
    return "_".join([now.strftime("%y%m%d%H%M%S"), random_string])


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception(e)
