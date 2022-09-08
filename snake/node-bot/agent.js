#!/usr/bin/env node

const fs = require("fs")

const AGENT_NAME = "noodles"
let AGENT_ID = null

let random_string = (Math.random() + 1).toString(36).substring(7);
const log_file = `${AGENT_NAME}__${random_string}.log`

function choice(array) {
  return array[Math.floor(Math.random() * array.length)];
}

function update(state, response) {
  response.move = choice(["UP", "RIGHT", "DOWN", "LEFT"])
}

try {
  fs.unlinkSync(log_file)
} catch(err) { }

process.stdin.on("data", raw_data => {
  raw_data = raw_data.toString()
  fs.writeFile(log_file, `got: ${raw_data}`, { flag: 'a+' }, err => {});
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

  let output = JSON.stringify(response) + "\n"
  fs.writeFile(log_file, `sending: ${output}`, { flag: 'a+' }, err => {});
  process.stdout.write(output)
})

setInterval(() => {}, 5); // HACK
