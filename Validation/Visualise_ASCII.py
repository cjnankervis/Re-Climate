#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Thu Nov 17 09:38:02 2022

@author: Dr Christopher Nankervis, WeatherLogistics.
Re-Climate® Product Developer & Owner.

Description.
Generates a country-wide plot of a Re-Climate® temperature or precipitation variable from an ASCII input.

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import datetime

now = datetime.datetime.now()
copy_yr = now.year

'''User to define 2 ascii plots to be compared'''
ascii_1 = "./Rainfall_AnomalyBenchmark.asc"
ascii_2 = "./Rainfall_AnomalyWeatherLogistics.asc"
#
data_paths = (ascii_1, ascii_2)
titles = ("C3S, 10th Centile", "C3S, 90th Centile")
variable_units = "Precipitation/ % of Climate"

fig, (ax1, ax2) = plt.subplots(1,2,dpi=2000,figsize=(15,5),constrained_layout=True)
plt.subplots_adjust(wspace=0.15)
fig.suptitle("Re-Climate® February Rainfall Forecast. Copyright "+str(copy_yr)+". All rights reserved.")
gs = gridspec.GridSpec(1,4,width_ratios=[0.15,5,0.15,5])

for ind, data_path in enumerate(data_paths):
    # Read in Re-Climate data header data
    with open(data_path, 'r') as data_f:
        data_header = data_f.readlines()[:6]
     
    # Read the Re-Climate ASCII raster header
    data_header = [item.strip().split()[-1] for item in data_header]
    data_cols = int(data_header[0])
    data_rows = int(data_header[1])
    data_xll = float(data_header[2])
    data_yll = float(data_header[3])
    data_cs = float(data_header[4])
    data_nodata = float(data_header[5])
     
    # Read in the data array
    data_array = np.loadtxt(data_path, dtype=np.float, skiprows=6)
    
    # Set the nodata values to nan
    data_array[data_array == data_nodata] = np.nan
    
    ax = ax1 if not ind else ax2
    # Plot Re-Climate ASCII grid with colorbar
    ax.set_title(titles[ind])
    
    # Show a colorbar legend
    img_plot = ax.imshow(data_array, cmap='jet')
     
    ax.grid(True)

    # Place a colorbar next to the map
    cbar = fig.colorbar(img_plot, cax=fig.add_subplot(gs[ind*2]), label=f"{variable_units}")
# Show forecast plots
plt.show()
