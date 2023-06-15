"""

PLOTS THE MEAN AND THE DIFFERENCES OF ALL COMBINATIONS FOR EACH ENSEMBLE MEMBER
SO IN RED THE MEAN DIFFERENCES AND IN YELLOW ALL THE OTHER COMBINATIONS
TO SHOW THE DIFFERENCE IN USING 20 RUNS OR ANOTHER AMOUNT OF ENSEMBLE MEMBERS

"""


import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

# Define function that calculates the average of the runs
def calculate_average(file_names):
    data = []
    for file_name in file_names:
        with open(file_name, 'r') as file:
            # Read the data from each file and convert to float
            file_data = [float(line.strip()) for line in file]
            data.append(file_data)
    data = np.array([arr[:1910] for arr in data])
    return np.average(data, axis=0)

# Decide how many runs you want to combine and how many averages you will use in the plot. 
num_runs = 20 # Specify the number of runs for the average
total_averages = 150  # Specify the total number of averages needed
averages = []

avg_run = np.loadtxt('tempchanges_2x.txt')

# Determine the common length between avg_run and the average data arrays
common_length = 1910 

# Generate combinations of run indices based on the number of runs
combinations_indices = combinations(list(range(1, 21)), num_runs)

# Calculate the average of each combination
for combi in combinations_indices:
    # Generate file names based on the current combination of run indices
    file_names = [f'2x_del_run{j}.txt' for j in combi]
    # Calculate the average for the current combination of runs
    average = calculate_average(file_names)
    # Append the average data array to the list of averages
    averages.append(average.tolist())
    if len(averages) == total_averages:
        break

###################################### PLOT ###################################### 

plt.figure(dpi=1200) # Increase quality of plot

# Plot the yellow lines using the first average from the averages list
plt.plot(range(1850, 3760), averages[0], linewidth=0.8, color='yellow', label='Differences of combinations')

# Plot the differences for each run
for i in range(len(averages)):
    plt.plot(range(1850,3760),averages[i], linewidth=0.8, color='yellow')
    
plt.plot(range(1850, 3760), avg_run[0:common_length], linewidth=0.6, color='red', label='Average difference') 

plt.xlim(1800, 3850) # Set the x-axis limits beyond the range of the available data

plt.xlabel('Time')
plt.ylabel('Temperature difference (K)')
#plt.title(f'{num_runs} ensemble members')
plt.legend(loc = 'lower right', fontsize='small')
plt.ylim(-0.05, 4.2)
plt.show()