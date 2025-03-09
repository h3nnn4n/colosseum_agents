# STDIO Random Agent

This is a simple agent for the Colosseum platform that uses the STDIO approach for communication. The agent makes random moves based on the game type detected from the world state.

## Features

- Uses stdin/stdout for direct communication
- Handles multiple game types by detecting the structure of the world state
- Demonstrates usage of various Python libraries
- Includes proper error handling

## Dependencies

This agent includes several dependencies to demonstrate Docker's value:

- Pandas & Matplotlib - For data processing and visualization
- SciPy & NumPy - For scientific calculations
- tqdm - For progress bars
- requests - For HTTP requests
- plotly - For interactive visualizations
- colorama - For colored terminal output

## Docker Usage

Build the Docker image:

```bash
docker build -t stdio-random-agent .
```

Run the container with stdio piping:

```bash
# Example with echoing a JSON message to the container
echo '{"ping": true}' | docker run -i stdio-random-agent
```

## Development

To run the agent directly without Docker:

```bash
python agent.py
```

## Testing

You can test the agent by piping JSON to it:

```bash
echo '{"ping": true}' | python agent.py
```

Expected response:

```json
{"pong": "pong"}
```

## Protocol

The agent follows the Colosseum protocol:
- Responds to `ping` with `pong`
- Stores and returns the `agent_id` when set
- Makes random moves based on the game state
- Handles the `stop` message