import json
import logging
import random
import string
import sys
from datetime import datetime


def get_internal_id():
    now = datetime.now()

    random_string = "".join(
        random.choices(
            string.ascii_lowercase + string.ascii_uppercase + string.digits, k=6
        )
    )
    return "_".join([now.strftime("%y%m%d%H%M%S"), random_string])


def send_commands(data):
    data_encoded = json.dumps(data)
    logging.debug(f"sending {data}")
    sys.stdout.write(data_encoded + "\n")
    sys.stdout.flush()


def get_state():
    logging.debug("waiting for data")
    data = sys.stdin.readline()
    logging.debug(f"got data: {data}")
    state = json.loads(data)
    return state
