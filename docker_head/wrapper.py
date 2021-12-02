import os
import socket

from pexpect.popen_spawn import PopenSpawn

WRAPEE_PATH = "./agent.py"
SERVER_ADDRESS = "/var/colosseum.socket"
SEPARATOR = os.environ.get("SEPARATOR")


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
    wrapped = PopenSpawn(WRAPEE_PATH)
    sock = socket.socket(socket.AF_UNIX)
    sock.connect(SERVER_ADDRESS)

    while True:
        for data in reader(sock):
            result = exchange_message(wrapped, data)
            print(f"{data} {result}")
            send(sock, result)


if __name__ == "__main__":
    main()
