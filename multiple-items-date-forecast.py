"""
Monte Carlo Simulation for Project Completion Dates
Version: 1.7
"""

import json
import random
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load user-defined config
with open('multiple-items-date-forecast.config.json', 'r') as f:
    config = json.load(f)

# Extract parameters from config
throughputs = config["throughputs"]
num_items = config["num_items"]
num_completed = config["num_completed"]
timeframe_weeks = config["timeframe_weeks"]
throughput_sigma = config["throughput_sigma"]
start_date = config.get("start_date", "")

# Constants
num_simulations = 10000

def calculate_completion_dates(base_date):
    completion_dates = []
    for _ in range(num_simulations):
        completed = num_completed
        current_week = 0
        while completed < num_items:
            throughput = random.choice(throughputs)
            completed += random.normalvariate(throughput / timeframe_weeks, throughput_sigma)
            current_week += 1
        completion_date = base_date + timedelta(weeks=current_week)
        completion_dates.append(completion_date)
    return completion_dates

# Derive base_date from start_date
base_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else datetime.today()

# Run simulation
completion_dates = calculate_completion_dates(base_date)
completion_dates_np = np.array([(date - base_date).days for date in completion_dates])

# Percentile projections
projected_completion_date_95 = base_date + timedelta(days=np.percentile(completion_dates_np, 95))
projected_completion_date_85 = base_date + timedelta(days=np.percentile(completion_dates_np, 85))
projected_completion_date_60 = base_date + timedelta(days=np.percentile(completion_dates_np, 60))

# Output
print("Start Date:", base_date.date())
print("Projected Completion Date (95% certainty):", projected_completion_date_95)
print("Projected Completion Date (85% certainty):", projected_completion_date_85)
print("Projected Completion Date (60% certainty):", projected_completion_date_60)

# Plot
plt.hist(completion_dates, bins=50, color='skyblue', edgecolor='black')
plt.axvline(projected_completion_date_95, color='yellow', linestyle='--', label=f'{projected_completion_date_95.date()} (95%)')
plt.axvline(projected_completion_date_85, color='red', linestyle='--', label=f'{projected_completion_date_85.date()} (85%)')
plt.axvline(projected_completion_date_60, color='green', linestyle='--', label=f'{projected_completion_date_60.date()} (60%)')
plt.title(f'Estimated Completion Dates of All {num_items} Items')
plt.xlabel('Estimated Completion Date')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
