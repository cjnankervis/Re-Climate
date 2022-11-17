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

data_paths = ("./Rainfall_AnomalyBenchmark.asc", "./Rainfall_AnomalyWeatherLogistics.asc")
titles = ("Rainfall Benchmark", "Rainfall WeatherLogistics")
variable_units = "Precipitation/ % of Climate"

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
     
    # Plot Re-Climate ASCII grid with colorbar
    fig, ax = plt.subplots(dpi=2000)
    ax.set_title("Re-Climate® "+titles[ind]+" Forecast. \nCopyright. All rights reserved.")
     
    # Get the img object in order to pass it to the colorbar function
    img_plot = ax.imshow(data_array, cmap='jet')
     
    # Place a colorbar next to the map
    cbar = fig.colorbar(img_plot, label=f"{variable_units}")
     
    ax.grid(True)
    plt.show()