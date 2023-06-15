import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

# Define function that calculates the average of the runs
def calculate_average(file_names):
    data = np.array([np.loadtxt(file_name) for file_name in file_names])
    return np.average(data, axis=0)

# Specify the number of runs for the average and the total number of averages needed
num_runs = 20
total_averages = 40000

# Load the average run data
avg_run = np.loadtxt('tempchanges_1pct.txt')
common_length = 1000

# Generate combinations of run indices based on the number of runs
combinations_indices = list(combinations(range(1, 21), num_runs))

# Calculate the averages for each combination
averages = []
for combi in combinations_indices[:total_averages]:
    file_names = [f'1pct_del_run{j}.txt' for j in combi]
    average = calculate_average(file_names)
    averages.append(average.tolist())


###################################### PLOT ######################################

plt.figure(dpi=1200) # Increase quality of plot

# Plot the yellow lines using the first average from the averages list
plt.plot(range(1850, 2850), averages[0], linewidth=0.8, color='yellow', label='Differences of combinations')

# Plot the differences for each run
for average in averages:
    plt.plot(range(1850, 2850), average, linewidth=0.8, color='yellow')

plt.plot(range(1850, 2850), avg_run[:common_length], linewidth=0.6, color='red', label='Average difference')

plt.xlim(1800, 3800) # Set the x-axis limits beyond the range of the available data

plt.xlabel('Time')
plt.ylabel('Temperature difference (K)')
plt.legend(loc='lower right')
plt.ylim(-0.05, 4.2)
plt.show()
