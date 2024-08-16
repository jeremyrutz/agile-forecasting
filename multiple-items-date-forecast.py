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

# Define function to calculate completion dates for simulations
def calculate_completion_dates():
    completion_dates = []
    for _ in range(num_simulations):
        completed = num_completed
        current_week = 0
        while completed < num_items: # and current_week < timeframe_weeks:
            # Randomly select throughput value from historical data
            throughput = random.choice(throughputs)
            completed += random.normalvariate(throughput / timeframe_weeks, 10)  # Assuming 10 as variability
            current_week += 1
        if completed >= num_items:
            completion_date = datetime.today() + timedelta(weeks=current_week)
            completion_dates.append(completion_date)
    return completion_dates

# Run simulations and calculate completion dates
completion_dates = calculate_completion_dates()

completion_dates.sort()

# Calculate the projected date at which the simulation is 95% sure
percentile_index_95 = int(0.95 * len(completion_dates))
projected_completion_date_95 = completion_dates[percentile_index_95]

# Calculate the projected date at which the simulation is 85% sure
percentile_index_85 = int(0.85 * len(completion_dates))
projected_completion_date_85 = completion_dates[percentile_index_85]

# Calculate the projected date at which the simulation is 60% sure
percentile_index_60 = int(0.6 * len(completion_dates))
projected_completion_date_60 = completion_dates[percentile_index_60]

# Output projected completion dates
print("Projected Completion Date (95% certainty):", projected_completion_date_95)
print("Projected Completion Date (85% certainty):", projected_completion_date_85)
print("Projected Completion Date (60% certainty):", projected_completion_date_60)

# Plot histogram of completion dates
plt.hist(completion_dates, bins=50, color='skyblue', edgecolor='black')
plt.axvline(projected_completion_date_95, color='yellow', linestyle='--', label='{} Completion Date (95% certainty)'.format(projected_completion_date_95.date()))
plt.axvline(projected_completion_date_85, color='red', linestyle='--', label='{} Completion Date (85% certainty)'.format(projected_completion_date_85.date()))
plt.axvline(projected_completion_date_60, color='green', linestyle='--', label='{} Completion Date (60% certainty)'.format(projected_completion_date_60.date()))
plt.title('Estimated Completion Dates of All {} Items'.format(num_items))
plt.xlabel('Estimated Completion Date')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()
