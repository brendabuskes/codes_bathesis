"""

Calculates new projections for a chosen number of ensemble members
Then, compares it to a chosen baseline measurement (e.g., the 20-projection or the average of the 20 runs from the experiment).
It also calculates the maximum error that occurs for that number of em.


"""

import numpy as np
import math
from itertools import combinations
import random


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

# Specify the combinations of runs
num_runs = 1
num_runs_combinations = list(combinations(range(1, 21), num_runs))
random.shuffle(num_runs_combinations)
#num_runs_combinations = num_runs_combinations[:100000]

# Calculate averages for each combination
averages = []
for combination in num_runs_combinations:
    file_names = [f'1pct_del_run{j}.txt' for j in combination]
    average = calculate_average(file_names)
    average[0] = 0
    averages.append(average)

# Calculate the derivatives and multiply by a constant for each average
derivatives = []
multiplied_derivatives = []
green_values = []
constant = 0.26966262

for average in averages:
    derivative = np.diff(average)
    derivatives.append(derivative)
    green = derivative * constant
    multiplied_derivatives.append(green)
    green_values.append(list(green))

##############################################################################

# Define function g
def g(t):
    return min(5.35 * math.log(1.01) * t, 5.35 * math.log(2))

# Calculate convolution for t from 0 to 999 for each set of green_values
conv_em_list = []

for green_values in multiplied_derivatives:
    conv_em = []
    for t in range(999):
        s = 0.0
        for n in range(t+1):
            s += green_values[n] * g(t-n)
        conv_em.append(s)
    conv_em_list.append(conv_em)


################################ DIFFERENCE ####################################

avg_run = np.loadtxt('tempchanges_1pct.txt')

# Determine the common length between avg_run and the average data arrays
common_length = 1000 

# Calculate differences between each run and the mean values
differences = np.zeros((len(conv_em_list), common_length))
for i in range(len(conv_em_list)):
    differences[i] = abs(conv_em_list[i][0:common_length] - avg_run[0:common_length])
    
################################ MAXIMUM ERROR ##################################

max_diff = []
# find max in list
for x in differences:
    max_diff.append(max(x))

# Calculate the average error for the chosen number of ensemble members
av_error = np.mean(max_diff)
print(av_error)