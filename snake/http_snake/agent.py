import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from random import choice

hostName = "localhost"
serverPort = 8080


_DIE = False

AGENT_NAME = "random"
AGENT_ID = None
MODE = "STDIO"


def bot(state):
    global _DIE
    global AGENT_ID

    response = {}

    if state.get("stop"):
        _DIE = True
        return response

    if state.get("set_agent_id"):
        AGENT_ID = state.get("set_agent_id")
        response["agent_name"] = AGENT_NAME

    if state.get("ping"):
        response["pong"] = "boofar"

    if AGENT_ID:
        response["agent_id"] = AGENT_ID

    response["move"] = choice(["UP", "RIGHT", "DOWN", "LEFT"])

    return response


class BotServer(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)

        content_len = int(self.headers.get("Content-Length"))
        post_body = self.rfile.read(content_len)
        payload = json.loads(post_body)
        response = bot(payload)

        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write((json.dumps(response)).encode())


def main():
    while True:
        data = sys.stdin.readline()
        state = json.loads(data)
        response = bot(state)
        send_commands(response)


def send_commands(data):
    data_encoded = json.dumps(data)
    sys.stdout.write(data_encoded + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    if MODE == "STDIO":
        main()

    if MODE == "HTTP":
        webServer = HTTPServer((hostName, serverPort), BotServer)

        with webServer as s:
            while not _DIE:
                s.handle_request()
