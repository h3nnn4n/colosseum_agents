import json

from flask import Flask, request
from pexpect.popen_spawn import PopenSpawn

agent = PopenSpawn(["./agent.py"])
app = Flask(__name__)


@app.route("/", methods=['GET'])
def get():
    return "Yes, it works. To communicate with the agent make a POST request."


@app.route("/", methods=['POST'])
def post():
    data = json.dumps(request.json)
    agent.sendline(data)
    agent_out = agent.readline()
    return agent_out
