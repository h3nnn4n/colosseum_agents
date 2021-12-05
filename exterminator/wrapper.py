import json
import logging
import os
import signal
import socket

from pexpect.popen_spawn import PopenSpawn

logging.basicConfig(filename="network_wrapper.log", level=logging.DEBUG)
logger = logging.getLogger("network_wrapper")

WRAPEE_PATH = "./agent.py"
SOCKET_FILE = os.environ.get("SOCKET_FILE", "colosseum.socket")
SERVER_ADDRESS = os.path.join("/var/colosseum", SOCKET_FILE)
SEPARATOR = os.environ.get("SEPARATOR", "\n")


def send(socket, msg):
    if SEPARATOR not in msg:
        msg += SEPARATOR

    msg = msg.encode()
    msglen = len(msg)
    totalsent = 0
    while totalsent < msglen:
        sent = socket.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent


def reader(socket, read_size=4):
    buffer = ""
    while True:
        # FIXME: This could deadlock if the message has two separators
        new_data = socket.recv(read_size).decode()
        buffer += new_data

        if SEPARATOR in buffer:
            data, _, buffer = buffer.partition(SEPARATOR)
            yield data


def exchange_message(child_process, data_in, send_only=True):
    child_process.sendline(data_in)

    if send_only:
        return

    data_out = child_process.readline().decode().strip()
    return data_out


def main():
    logger.info("starting")
    wrapped = PopenSpawn(WRAPEE_PATH)
    sock = socket.socket(socket.AF_UNIX)
    logger.info(f"connecting to {SERVER_ADDRESS}")
    sock.connect(SERVER_ADDRESS)
    logger.info("connected")

    logger.debug("loop")
    for data in reader(sock):
        logger.debug(f"got data: {data}")
        # If we have a stop we should only send a message to the agent, but
        # wait for no response.
        done = check_stop(data)
        result = exchange_message(wrapped, data, send_only=done)

        if done:
            break

        logger.debug(f"sending {result=}")
        send(sock, result)

    logger.info("killing agent")
    wrapped.kill(signal.SIGTERM)
    logger.info("done")


def check_stop(raw_message):
    try:
        payload = json.loads(raw_message)
        if payload.get("stop"):
            logging.info("found stop command")
            return True
    except Exception as e:
        return False


if __name__ == "__main__":
    main()
