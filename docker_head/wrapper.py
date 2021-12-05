import os
import logging
import socket

from pexpect.popen_spawn import PopenSpawn

logger = logging.getLogger('network_wrapper')
logger.setLevel(logging.DEBUG)

WRAPEE_PATH = "./agent.py"
SOCKET_FILE = os.environ.get("SOCKET_FILE", "colosseum.socket")
SERVER_ADDRESS = f"/var/colosseum/{SOCKET_FILE}"
SEPARATOR = os.environ.get("SEPARATOR", "\n")


def send(socket, msg):
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


def exchange_message(child_process, data_in):
    child_process.sendline(data_in)
    data_out = child_process.readline().decode().strip()
    return data_out


def main():
    logger.info("starting")
    wrapped = PopenSpawn(WRAPEE_PATH)
    sock = socket.socket(socket.AF_UNIX)
    logger.info(f"connecting to {SERVER_ADDRESS}")
    sock.connect(SERVER_ADDRESS)
    logger.info("connected")

    while True:
        for data in reader(sock):
            logger.debug(f"got {data=}")
            result = exchange_message(wrapped, data)
            logger.debug(f"sending {result=}")
            send(sock, result)

    logger.info("done")


if __name__ == "__main__":
    main()
