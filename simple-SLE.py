# simple-sle.py Version 1.2 (Loads data and timebox_duration from JSON)

import json
import os

# Load configuration from external JSON file
config_path = 'simple-sle.config.json'
if not os.path.exists(config_path):
    raise FileNotFoundError(f"Config file not found: {config_path}")

with open(config_path, 'r') as f:
    config = json.load(f)

historical_data = config["historical_data"]
timebox_duration = config["timebox_duration"]

# Calculate total time spent in the workflow
total_time_to_done = sum(data["time_spent"] for data in historical_data)

# Calculate adjustment factor
adjustment_factor = timebox_duration / total_time_to_done

# Adjust SLEs based on historical data and adjustment factor
sles = {}
for data in historical_data:
    state = data["state"]
    time_spent = data["time_spent"]
    adjusted_time_spent = time_spent * adjustment_factor
    sles[state] = min(adjusted_time_spent, timebox_duration)

# Output adjusted SLEs
for state, sle in sles.items():
    print(f"SLE for {state}: {sle:.2f} days")
