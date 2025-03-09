#!/usr/bin/env python3

import json
import random
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
import pandas as pd

# This is a dummy import to demonstrate dependency usage
from scipy import stats
from tqdm import tqdm

AGENT_NAME = "docker-foo"


@dataclass
class GameState:
    """Simple wrapper for game state data"""

    agent_id: Optional[str] = None
    world_state: Dict[str, Any] = None

    def is_valid(self) -> bool:
        """Check if we have necessary data to make a move"""
        return self.agent_id is not None and self.world_state is not None


class RandomAgent:
    def __init__(self):
        self.agent_id = None
        self.move_history = []
        self.state_history = []

        # Demonstrate usage of dependencies
        self.random_distribution = stats.norm(0, 1)

    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming message and return response"""
        response = {}

        # Handle agent ID setting
        if message.get("set_agent_id"):
            self.agent_id = message.get("set_agent_id")
            response["agent_name"] = AGENT_NAME

        # Always include agent ID in responses once we have it
        if self.agent_id:
            response["agent_id"] = self.agent_id

        # Handle ping messages
        if message.get("ping"):
            response["pong"] = "pong"

        # Process game state and generate move if we have world_state
        if message.get("world_state"):
            world_state = message.get("world_state")
            self.state_history.append(world_state)

            # Detect game type and make appropriate move
            move = self.generate_move(world_state)
            if move:
                response.update(move)
                self.move_history.append(move)

            # Simulate some "thinking" with the tqdm library
            for _ in tqdm(range(10), desc="Thinking", file=sys.stderr):
                time.sleep(0.01)

        return response

    def generate_move(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a move based on the world state"""
        # Try to detect the game type from the world state
        if "snakes" in world_state:
            # Snake game - return random direction
            return {"move": random.choice(["UP", "RIGHT", "DOWN", "LEFT"])}

        elif "cherries" in world_state:
            # Cherry picker game - return random position
            return {
                "actions": [
                    {
                        "type": "pick",
                        "position": [random.randint(0, 10), random.randint(0, 10)],
                    }
                ]
            }

        elif "food" in world_state:
            # Food catcher game - random move in one of 8 directions
            return {
                "actions": [
                    {
                        "type": "move",
                        "direction": random.choice(
                            [0, 45, 90, 135, 180, 225, 270, 315]
                        ),
                    }
                ]
            }

        elif "board" in world_state:
            # Chess game - random move (this is very naive)
            return {"actions": [{"from": "e2", "to": "e4"}]}

        else:
            # Generic fallback - empty actions
            return {"actions": []}

    def visualize_history(self):
        """Use matplotlib to visualize game history (dummy function)"""
        if not self.state_history:
            return

        # Create a dummy DataFrame to demonstrate pandas usage
        data = pd.DataFrame(
            {
                "turn": range(len(self.state_history)),
                "data_size": [len(str(s)) for s in self.state_history],
            }
        )

        # Dummy plot that's never shown
        plt.figure(figsize=(10, 6))
        plt.plot(data["turn"], data["data_size"])
        plt.title("State Data Size by Turn")
        plt.xlabel("Turn")
        plt.ylabel("Data Size (bytes)")
        plt.close()


def main():
    agent = RandomAgent()

    # Main loop
    while True:
        try:
            # Read a line from stdin
            data = sys.stdin.readline()
            if not data:
                break

            # Parse the JSON message
            message = json.loads(data)

            # Stop if requested
            if message.get("stop"):
                # Do some cleanup or analysis with our dependencies
                agent.visualize_history()
                break

            # Process the message and get response
            response = agent.process_message(message)

            # Send the response
            print(json.dumps(response), flush=True)

        except json.JSONDecodeError:
            print(json.dumps({"error": "Invalid JSON received"}), flush=True)
            continue
        except Exception as e:
            print(json.dumps({"error": str(e)}), flush=True)
            continue


if __name__ == "__main__":
    main()
