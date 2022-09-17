import json
from random import choice
from http.server import BaseHTTPRequestHandler, HTTPServer


hostName = "localhost"
serverPort = 8080


_DIE = False

AGENT_NAME = "random"
AGENT_ID = None


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

    return (response)


class BotServer(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)

        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        payload = json.loads(post_body)
        response = bot(payload)

        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write((json.dumps(response)).encode())


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), BotServer)

    with webServer as s:
        while not _DIE:
            s.handle_request()
