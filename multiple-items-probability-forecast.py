import json
import random
import numpy as np
import matplotlib.pyplot as plt

# Load configuration from a JSON file
with open('multiple-items-probability-forecast.config.json', 'r') as config_file:
    config = json.load(config_file)

# Read parameters from config
historical_throughput = config['historical_throughput']
throughput_sigma = config['throughput_sigma']

# Number of simulations
num_simulations = 10000

# Perform Monte Carlo Simulation
simulated_throughput = []
for _ in range(num_simulations):
    historical_value = random.choice(historical_throughput)
    simulated_value = random.normalvariate(historical_value, throughput_sigma)
    simulated_throughput.append(simulated_value)

# Sort the simulated throughput values
simulated_throughput.sort()

# Calculate percentiles
p60 = np.percentile(simulated_throughput, 60)
p85 = np.percentile(simulated_throughput, 85)
p95 = np.percentile(simulated_throughput, 95)

# Display results
print("Probability of throughput at P60:", p60)
print("Probability of throughput at P85:", p85)
print("Probability of throughput at P95:", p95)

# Plot histogram
plt.hist(simulated_throughput, bins=30, alpha=0.7, color='blue', edgecolor='black')
plt.axvline(x=p60, color='red', linestyle='--', label='P60 = {}'.format(round(p60)))
plt.axvline(x=p85, color='green', linestyle='--', label='P85 = {}'.format(round(p85)))
plt.axvline(x=p95, color='orange', linestyle='--', label='P95 = {}'.format(round(p95)))
plt.xlabel('Throughput')
plt.ylabel('Frequency')
plt.title('Histogram of Simulated Throughput (Version 1.1)')
plt.legend()
plt.grid(True)
plt.show()
