""""

WHAT DOES THIS CODE DO?
- DETERMINES ALL COMBINATIONS AND THEIR AVERAGE FOR EACH NUMBER OF ENSEMBLE MEMBERS
- CALCULATES THE DIFFERENCE FOR EACH COMBINATION
- CALCULATES MOVING AVERAGE
- CALCUALTES STANDARD DEVIATION
- PLOTS MOVING AVERAGE + STANDARD DEVIATION
- CALCULATES MAXIMUM ERROR FOR EACH NUMBER OF ENSEMBLE MEMBERS


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
averages = []

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

avg_run = np.loadtxt('tempchanges_2x.txt')

# Determine the common length between avg_run and the average data arrays
common_length = 1910 

# Calculate differences between each run and the mean values
differences = np.zeros((len(averages), common_length))
for i in range(len(averages)):
    differences[i] = abs(averages[i][0:common_length] - avg_run[0:common_length])


################################ #TOTAL AVERAGE ##################################

# Calculate the average of all the different combinations
av_differences = list(np.mean(differences, axis=0))

################################ MOVING AVERAGE ##################################

window_size = 20
i = 0
moving_av = [] # Initialize an empty list to store moving averages
  
# Loop through the array to consider
# every window of size 1000
while i < len(av_differences) - window_size + 1:
    # Store elements from i to i+window_size in list to get the current window
    window = av_differences[i : i + window_size]  
    # Calculate the average of current window
    window_average = round(sum(window) / window_size, 3)
    # Store the average of current window in moving average list
    moving_av.append(window_average)  
    # Shift window to right by one position
    i += 1

############################ STANDARD DEVIATION ##################################


#The standard deviation of average of all combinations
std_diff = np.std(differences, dtype=np.float64)

# Make a list of the values: moving average + 1 standard deviation
std = []
for num in moving_av:
    std.append(num + std_diff)

################################ MAXIMUM ERROR ##################################

max_diff = []
# find max in list
for x in differences:
    max_diff.append(max(x))

# Calculate the average error for the chosen number of ensemble members
av_error = np.mean(max_diff)
print(av_error)

###################################### PLOT ###################################### 

# Plot the differences for each run
#for i in range(len(averages)):
#    plt.plot(differences[i], linewidth=0.3, label=f'Run {i+1}')

plt.figure(dpi=1200) # Increase quality of plot

# Plot the average of all combinations against time
plt.plot(range(1850, 3741), moving_av, linewidth=1, color='red', label='Moving average of average differences') 
plt.plot(range(1850, 3741), std, linewidth=1, color='blue', label='Moving average + \u03C3')

# Plot black line at y=0
plt.axhline(y=0, color='black', linewidth=0.8, linestyle='--')
   
av_max = np.max(av_differences) # The maximum average difference 
std_text = plt.text(0.02, 0.95, f'Standard Deviation: {std_diff:.3f}', ha='left', va='center', transform=plt.gca().transAxes,fontsize=8)

plt.xlim(1800, 3870) # Set the x-axis limits beyond the range of the available data

plt.xlabel('Time')
plt.ylabel('Error')
#plt.title(f'{num_runs} ensemble members')
plt.ylim(-0.05, 0.3)
plt.legend(loc = 'upper right', fontsize='small')
plt.show()

