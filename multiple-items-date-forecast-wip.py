"""
Multiple Items Date Forecast with WIP Consideration
Filename: multiple-items-date-forecast-wip.py
Version: 0.1
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Historical throughput data
throughputs = [55, 86, 132, 152, 132]  # Units completed per increment

# Parameters
num_simulations = 10000
num_items = 187
num_completed = 18
max_wip = 100  # Maximum allowable work-in-progress
timeframe_weeks = 12  # Proxy for cycle time

def calculate_completion_dates_with_wip():
    """
    Simulates completion dates for a project using Monte Carlo methods
    and considers WIP constraints using Little's Law.

    The function calculates the time required to complete a specified number of
    items (`num_items`) based on historical throughput data. It incorporates
    randomness to model variability in throughput while respecting a maximum WIP constraint.

    Returns:
        list[datetime]: A list of datetime objects representing projected completion dates.
    """
    completion_dates = []
    for _ in range(num_simulations):
        completed = num_completed
        current_week = 0
        while completed < num_items:
            # Randomly select throughput value from historical data
            throughput = random.choice(throughputs)
            
            # Calculate effective throughput based on WIP and Little's Law
            effective_throughput = min(max_wip / timeframe_weeks, throughput)
            
            # Add variability to throughput
            completed += random.normalvariate(effective_throughput, 10)  # Assuming 10 as variability
            current_week += 1
        
        if completed >= num_items:
            completion_date = datetime.today() + timedelta(weeks=current_week)
            completion_dates.append(completion_date)
    return completion_dates

# Run simulations and calculate completion dates
completion_dates = calculate_completion_dates_with_wip()

# Calculate percentiles directly using np.percentile
completion_dates_np = np.array([(date - datetime.today()).days for date in completion_dates])  # Convert to days
projected_completion_date_95 = datetime.today() + timedelta(days=np.percentile(completion_dates_np, 95))
projected_completion_date_85 = datetime.today() + timedelta(days=np.percentile(completion_dates_np, 85))
projected_completion_date_60 = datetime.today() + timedelta(days=np.percentile(completion_dates_np, 60))

# Output projected completion dates
print("Projected Completion Date (95% certainty):", projected_completion_date_95)
print("Projected Completion Date (85% certainty):", projected_completion_date_85)
print("Projected Completion Date (60% certainty):", projected_completion_date_60)

# Plot histogram of completion dates
plt.hist(completion_dates, bins=50, color='skyblue', edgecolor='black')
plt.axvline(projected_completion_date_95, color='yellow', linestyle='--', label='{} Completion Date (95% certainty)'.format(projected_completion_date_95.date()))
plt.axvline(projected_completion_date_85, color='red', linestyle='--', label='{} Completion Date (85% certainty)'.format(projected_completion_date_85.date()))
plt.axvline(projected_completion_date_60, color='green', linestyle='--', label='{} Completion Date (60% certainty)'.format(projected_completion_date_60.date()))
plt.title('Estimated Completion Dates of All {} Items with WIP Consideration'.format(num_items))
plt.xlabel('Estimated Completion Date')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
