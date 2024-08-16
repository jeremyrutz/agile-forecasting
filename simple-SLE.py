# simple-sle.py Version 1.0

from collections import defaultdict

# Sample historical data
historical_data = [
    {"state": "To Do", "time_spent": 5},
    {"state": "In Progress", "time_spent": 17},
    {"state": "Review", "time_spent": 4}
    # Add more historical data as needed
]

# Calculate total time spent in the workflow
total_time_to_done = sum(data["time_spent"] for data in historical_data)

# Set timebox duration (in days)
timebox_duration = 14

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
