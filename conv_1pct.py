import math
#import matplotlib.pyplot as plt
#import numpy as np

# values for x-axis 
year = []
x = range(1,2000)
for n in x:
    year.append(n)

# Load values of f from file
with open('green.txt', 'r') as f_file:
    f = [float(line.strip()) for line in f_file]

# Define function g
def g(t):
    return min(5.35 * math.log(1.01) * t, 5.35 * math.log(2))

# Initialize output list
convolution = []

# Calculate convolution for t from 0 to 1998
for t in range(1999):
    # Initialize sum for this value of t
    s = 0.0
    for n in range(t+1):
        s += f[n] * g(t-n)
    convolution.append(str(s))

#Add in txt file
with open('convolution.txt', 'w') as f:
    for conv in convolution:
        f.write(conv)
        f.write('\n')
        

# Increase quality of plot
#plt.figure(dpi=1200)

# plotting the points 
#plt.plot(year,convolution,c='r',linewidth=0.7)

# Set the x-axis limits beyond the range of the available data
#plt.xlim(1, 2000)

# naming the x axis
#plt.xlabel('t')
# naming the y axis
#plt.ylabel('G^[T](t)')
  
# giving a title to my graph
#plt.title("Green's function")

#set y-axis ticks (step size=5)
#plt.yticks(np.arange(0, 3, 0.5))