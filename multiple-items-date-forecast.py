
""" 
Monte Carlo Simulation for Project Completion Dates
Version: 1.6
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Historical throughput data
throughputs = [55, 86, 132, 152, 132]

# Parameters
num_simulations = 10000
num_items = 187
num_completed = 18
timeframe_weeks = 12
start_date = "2025-08-01"  # Format: 'YYYY-MM-DD' or leave as "" to use today's date

def calculate_completion_dates(base_date):
    """
    Simulates completion dates for a project using Monte Carlo methods.

    Args:
        base_date (datetime): The date from which to start the simulation.

    Returns:
        list[datetime]: A list of datetime objects representing projected completion dates.
    """
    completion_dates = []
    for _ in range(num_simulations):
        completed = num_completed
        current_week = 0
        while completed < num_items:
            throughput = random.choice(throughputs)
            completed += random.normalvariate(throughput / timeframe_weeks, 10)
            current_week += 1
        completion_date = base_date + timedelta(weeks=current_week)
        completion_dates.append(completion_date)

    return completion_dates

# Derive base_date from start_date
base_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else datetime.today()

# Run simulations and calculate completion dates
completion_dates = calculate_completion_dates(base_date)

# Calculate percentiles directly using np.percentile
completion_dates_np = np.array([(date - base_date).days for date in completion_dates])
projected_completion_date_95 = base_date + timedelta(days=np.percentile(completion_dates_np, 95))
projected_completion_date_85 = base_date + timedelta(days=np.percentile(completion_dates_np, 85))
projected_completion_date_60 = base_date + timedelta(days=np.percentile(completion_dates_np, 60))

# Output projected completion dates
print("Start Date:",base_date.date())
print("Projected Completion Date (95% certainty):", projected_completion_date_95)
print("Projected Completion Date (85% certainty):", projected_completion_date_85)
print("Projected Completion Date (60% certainty):", projected_completion_date_60)

# Plot histogram of completion dates
plt.hist(completion_dates, bins=50, color='skyblue', edgecolor='black')
plt.axvline(projected_completion_date_95, color='yellow', linestyle='--', label='{} (95%)'.format(projected_completion_date_95.date()))
plt.axvline(projected_completion_date_85, color='red', linestyle='--', label='{} (85%)'.format(projected_completion_date_85.date()))
plt.axvline(projected_completion_date_60, color='green', linestyle='--', label='{} (60%)'.format(projected_completion_date_60.date()))
plt.title('Estimated Completion Dates of All {} Items'.format(num_items))
plt.xlabel('Estimated Completion Date')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
