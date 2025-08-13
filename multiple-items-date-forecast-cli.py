"""
Monte Carlo Simulation for Project Completion Dates
Version: 1.9 (CLI CSV input + JSON config with truncated normal throughput)
"""

import csv
import os
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy.stats import truncnorm  # <-- NEW: for truncated normal distribution

# Constants
num_simulations = 10000

# === Load configuration ===
config_path = 'multiple-items-date-forecast-cli.config.json'
if not os.path.exists(config_path):
    raise FileNotFoundError(f"Config file not found: {config_path}")

with open(config_path, 'r') as f:
    config = json.load(f)

num_items = config["num_items"]
num_completed = config["num_completed"]
timeframe_weeks = config["timeframe_weeks"]
throughput_sigma = config["throughput_sigma"]
start_date = config.get("start_date", "")

# === Load throughput data from CSV passed via CLI ===
csv_file_path = sys.argv[1] if len(sys.argv) > 1 else "throughput_data.csv"

def load_throughput_data(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")
    throughputs = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for value in row:
                value = value.strip()
                if value:
                    throughputs.append(float(value))
    if not throughputs:
        raise ValueError("No valid throughput values found in CSV.")
    return throughputs

throughputs = load_throughput_data(csv_file_path)

def sample_throughput(mean, sigma):
    a = (0 - mean) / sigma if sigma > 0 else -np.inf
    return truncnorm.rvs(a, np.inf, loc=mean, scale=sigma) if sigma > 0 else mean

# === Simulation Logic ===
def calculate_completion_dates(base_date):
    completion_dates = []
    for _ in range(num_simulations):
        completed = num_completed
        current_week = 0
        while completed < num_items:
            throughput = np.random.choice(throughputs)
            delta = sample_throughput(throughput / timeframe_weeks, throughput_sigma)
            completed += delta
            current_week += 1
        completion_date = base_date + timedelta(weeks=current_week)
        completion_dates.append(completion_date)
    return completion_dates

# === Run Simulation ===
base_date = datetime.strptime(start_date, "%Y-%m-%d") if start_date else datetime.today()
completion_dates = calculate_completion_dates(base_date)

# === Analyze Results ===
completion_days = np.array([(date - base_date).days for date in completion_dates])
projected_completion_date_95 = base_date + timedelta(days=np.percentile(completion_days, 95))
projected_completion_date_85 = base_date + timedelta(days=np.percentile(completion_days, 85))
projected_completion_date_60 = base_date + timedelta(days=np.percentile(completion_days, 60))

# === Output ===
print("Start Date:", base_date.date())
print("Projected Completion Date (95% certainty):", projected_completion_date_95)
print("Projected Completion Date (85% certainty):", projected_completion_date_85)
print("Projected Completion Date (60% certainty):", projected_completion_date_60)

# === Visualization ===
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
