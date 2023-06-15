""""""""""

MAKE NEW PROJECTIONS FOR ANOTHER NUMBER OF ENSEMBLE MEMBERS

You can adjust the number in the code and also adjust the number of new preditions

"""""""""""


import numpy as np
import math
import matplotlib.pyplot as plt
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
num_runs_combinations = num_runs_combinations[:20]

# Calculate averages for each combination
averages = []
for combination in num_runs_combinations:
    file_names = [f'2x_del_run{j}.txt' for j in combination]
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

# Calculate convolution for t from 0 to 1998 for each set of green_values
conv_em_list = []

for green_values in multiplied_derivatives:
    conv_em = []
    for t in range(1909):
        s = 0.0
        for n in range(t+1):
            s += green_values[n] * g(t-n)
        conv_em.append(s)
    conv_em_list.append(conv_em)


##############################################################################

# values for x-axis
year2 = []
x = range(1850, 3759)
for n in x:
    year2.append(n)    


# values for y-axis
conv = []
f = open('convolution.txt', 'r')
for row in f:
    row = row.split(' ')
    conv.append(row[0])

conv = list(map(float, conv))
conv = conv[:1909]

# Increase quality of plot
plt.figure(dpi=1200)

# plotting the points
plt.plot(year2, conv_em_list[0], c='red', linewidth=0.9, label= f'{num_runs} ensemble members')

# Plot the differences for each run
for i in range(1,len(conv_em_list)):
    plt.plot(year2,conv_em_list[i], linewidth=0.9, color='red')

plt.plot(year2, conv, c='b', linewidth=0.8, label='prediction')

plt.xlim(1800, 3850)

plt.legend(loc='lower right')
plt.grid()

# naming the x axis
plt.xlabel('Time (year)')
# naming the y axis
plt.ylabel('\u0394 Temp (K)')

# set y-axis ticks (step size=5)
plt.yticks(np.arange(0, 4, 0.5))