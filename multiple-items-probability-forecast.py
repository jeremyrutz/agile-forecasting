# Version 1.1 with Histogram (Raw Count on Y-axis)

import random
import numpy as np
import matplotlib.pyplot as plt

# Historical throughput values
historical_throughput = [6,11,7,9,9,2]

# Number of simulations
num_simulations = 10000

# Perform Monte Carlo Simulation
simulated_throughput = []
for _ in range(num_simulations):
    # Randomly pick one throughput value from historical data
    historical_value = random.choice(historical_throughput)
    # Generate simulated throughput value using random.normalvariate
    simulated_value = random.normalvariate(historical_value, 2)  # Using standard deviation of 5
    simulated_throughput.append(simulated_value)

# Sort the simulated throughput values
simulated_throughput.sort()

# Calculate the probability of throughput at P60, P85, and P95
p60 = np.percentile(simulated_throughput, 60)
p85 = np.percentile(simulated_throughput, 85)
p95 = np.percentile(simulated_throughput, 95)

# Display results
print("Probability of throughput at P60:", p60)
print("Probability of throughput at P85:", p85)
print("Probability of throughput at P95:", p95)

# Plot histogram with raw count on y-axis
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
