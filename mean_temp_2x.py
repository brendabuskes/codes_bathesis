"""""

BACHELOR THESIS CODE
Brenda Buskes

2x CO2 EXPERIMENT
MEAN TEMPERATURE AT 2M FOR ALL FILES

"""""

#################################################################

import xarray as xr
import numpy as np
import glob

# Make list of all the grb files in folder (for a given path)
grbfiles = []
path = r"E:/LRT/Data/abrupt2xCO2/2xCO2_run19_echam6_echam_1-2000"
for file in glob.glob(path + "/*.grb"):
    grbfiles.append(file)

# List that collects all the mean temperatures     
global_temps = []

# For every file in grbfiles, the function 'mean_temp' is going to calculate the mean temp
for filename in grbfiles:
    def mean_temp(filename):
        # Open the .grb file as an xarray dataset
        ds = xr.open_dataset(filename, decode_cf=False, engine='cfgrib', backend_kwargs={'errors': 'ignore'})
        # Select the temperature variable
        temp = ds['t2m']
        # Calculate the yearly average temperature
        yearly_mean = temp.mean(dim='time')
        # Calculate the weighted latitude average temperature (with use of radians)
        weights = np.cos(np.deg2rad(temp.latitude))
        weighted_mean = yearly_mean.weighted(weights).mean(dim='latitude')
        # Calculate the global average temperature
        global_mean = weighted_mean.mean(dim='longitude')
        # Return the result in Kelvin and add it to the list that collects the mean temperatures
        return(f"{global_mean.values:.8f}")
    global_temps.append(mean_temp(filename))

# Create a txt file where every temperature is added 
with open('all_temps_2x_run19.txt', 'w') as f:
    for temp in global_temps:
        f.write(temp)
        f.write('\n')
