# advanced-SLE.py Version 1.0

from collections import defaultdict
import csv
import numpy as np

# Function to read historical data from a comma-delimited text file
def read_historical_data(file_path):
    historical_data = []
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            historical_data.append(row)
    return historical_data

# Sample historical data file path
#
# The input data in the comma-delimited text file should follow a specific format to be properly read by the script. 
# Each row in the file represents a work item and should contain at least two columns: 
#   one for the state of the work item and another for the time spent in that state. 
# Optionally, you can include additional columns if needed.
#
# Here's an example of how the input data should be formatted in the text file:
# state,time_spent
# To Do,5
# In Progress,17
# Review,4
# To Do,8
# In Progress,12
# Review,6

historical_data_file = 'historical_data.csv'

# Read historical data from the file
historical_data = read_historical_data(historical_data_file)

# Extract time spent for each state
time_spent = defaultdict(list)
for data in historical_data:
    state = data["state"]
    time_spent[state].append(int(data["time_spent"]))

# Set timebox duration (in days)
timebox_duration = 14

# Calculate SLEs based on percentiles
percentiles = [50, 85, 95]  # Example percentiles
sles = {}
for state, times in time_spent.items():
    times = np.array(times)
    state_sles = np.percentile(times, percentiles)
    sles[state] = {percentile: min(timebox_duration, value) for percentile, value in zip(percentiles, state_sles)}

# Output SLEs
for state, sle_values in sles.items():
    print(f"SLEs for {state}:")
    for percentile, sle in sle_values.items():
        print(f"{percentile}th percentile: {sle:.2f} days")
