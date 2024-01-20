#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Sat Jan 20 20:22:02 2024

@author: Dr Christopher Nankervis, WeatherLogistics.
Re-Climate® Product Developer & Owner.

Description.
Generates a country-wide plot of the Re-Climate® precipitation variable from an ASCII input.

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import datetime
import cartopy.crs as ccrs
import cartopy.feature as cf
import calendar

country = 'UK'
start_year = '2023'
start_months = ('11','12')
lead_times = (1,2)

for lead_time in lead_times:
    
    for start_month in start_months:

        lead_month = (int(start_month)+lead_time-1) % 12
        if lead_month < int(start_month):
            year_lead = int(start_year) + 1
        else:
            year_lead = int(start_year)
        month_long = calendar.month_name[lead_month+1]
        print(month_long)
        
        now = datetime.datetime.now()
        copy_yr = now.year
        
        '''User to define 2 ascii plots to be compared'''
        ascii_file = f'raw_data/ReClimate_{start_month}_{start_year}_{lead_time}.asc'
        #
        title = (f'% Precipitation Compared to Recent Climate Mean\n{month_long} {year_lead}')
        variable_units = "Precipitation/ % of Climate"
        
        plt.figure(dpi=350)
        ax = plt.axes(projection=ccrs.Mercator(), frameon=True)
        # ax.suptitle("Re-Climate® February Rainfall Forecast. Copyright "+str(copy_yr)+". All rights reserved.")
        
        # Read in Re-Climate data header data
        with open(ascii_file, 'r') as data_f:
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
        data_array = np.loadtxt(ascii_file, dtype=np.float, skiprows=6)
        
        # Set the nodata values to nan
        data_array[data_array == data_nodata] = np.nan
        
        # Plot Re-Climate ASCII grid with colorbar
        ax.set_title(title)
        
        # Show a colorbar legend
        img_plot = ax.imshow(data_array, cmap='seismic_r', vmin=90, vmax=110)
         
        ax.grid(True)
        
        # Place a colorbar next to the map
        plt.suptitle('RE-CLIMATE Seasonal Climate Forecast', y=1.05, fontsize=18)
        plt.colorbar(img_plot,orientation="horizontal",ax=ax,
                    pad=0,
                    aspect=50)
        
        # Save
        plt.savefig(f'raw_data/ReClimate_{start_month}_{start_year}_{lead_time}.png', dpi=350)
        
        # Show forecast plots
        plt.show()
