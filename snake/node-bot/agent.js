#!/usr/bin/env node

const fs = require("fs")

const AGENT_NAME = "noodles"
let AGENT_ID = null

let random_string = (Math.random() + 1).toString(36).substring(7);
const log_file = `${AGENT_NAME}__${random_string}.log`

function choice(array) {
  return array[Math.floor(Math.random() * array.length)];
}

function update(state) {
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

  response.move = choice(["UP", "RIGHT", "DOWN", "LEFT"])

  return response
}

function log_to_file(message) {
  fs.writeFile(log_file, message, { flag: 'a+' }, err => {});
}

process.stdin.on("data", raw_data => {
  raw_data = raw_data.toString()
  log_to_file(`got: ${raw_data}`)
  state = JSON.parse(raw_data)

  let response = {}

  try {
    response = update(state)
  } catch(err) {
    response = {}
    log_to_file(`got error: ${err}\n`)
  }

  let output = JSON.stringify(response) + "\n"
  log_to_file(`sending: ${output}`)
  process.stdout.write(output)
})

setInterval(() => {}, 5); // HACK
