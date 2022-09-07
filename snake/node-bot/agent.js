#!/usr/bin/env node

const AGENT_NAME = "noodles"
let AGENT_ID = null

function choice(array) {
  return array[Math.floor(Math.random() * array.length)];
}

function update(state, response) {
  response.move = choice(["UP", "RIGHT", "DOWN", "LEFT"])
}

process.stdin.on("data", raw_data => {
  raw_data = raw_data.toString()
  state = JSON.parse(raw_data)

  let response = {}

  if (state.stop)
    process.exit()

  if (state.set_agent_id) {
    response.agent_name = AGENT_NAME
    AGENT_ID = state.set_agent_id
  }

  if (AGENT_ID)
    response.agent_id = AGENT_ID

  if (state.ping)
    response.pong = "noodles"

  update(state, response)

  process.stdout.write(JSON.stringify(response) + "\n")
})

setInterval(() => {}, 5); // HACK
