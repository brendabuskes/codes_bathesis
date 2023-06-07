"""""

BACHELOR THESIS CODE
Brenda Buskes

1PCT CO2 EXPERIMENT
YEARLY GLOBAL MEAN TEMPERATURE AT 2M FOR ALL FILES

"""""

#################################################################

import xarray as xr
import numpy as np
import glob

# Make list of all the nc files in folder
ncfiles = []
path = r""
for file in glob.glob(path + "/*.nc"):
    ncfiles.append(file)
    
# List that collects all the mean temperatures     
global_temps = []

# For every file in grbfiles, the function 'mean_temp' is going to calculate the mean temp
for filename in ncfiles:
    def average_temp(filename):
        # Open the .grb file as an xarray dataset
        ds = xr.open_dataset(filename, decode_cf=False)
        # Select the temperature variable
        temp = ds['2t']
        # Calculate the yearly average temperature
        yearly_mean = temp.mean(dim='time')
        # Calculate the weighted latitude average temperature
        weights = np.cos(np.deg2rad(temp.lat))
        weighted_mean = yearly_mean.weighted(weights).mean(dim='lat')
        # Calculate the global average temperature
        global_mean_kel = weighted_mean.mean(dim='lon')
        # Return the result in Kelvin
        return(f"{global_mean_kel.values:.8f}")
    global_temps.append(average_temp(filename))

# Create a txt file where every temperature is added        
with open('all_temps_1pct_run20.txt', 'w') as f:
    for mean_temp in global_temps:
        f.write(mean_temp)
        f.write('\n')
        
