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
import datetime
import cartopy.crs as ccrs
import calendar

country = 'UK' # Analysis data is currently available for the UK only
start_years = ['2024'] # ['2023','2023','2023','2024','2024','2024','2024','2024','2024','2024','2024'] # Forecast initiation years
start_months = ['10'] # ['10','11','12','01','02','03','04','05','06','07','08','09'] # Forecast start/ valid month
lead_times = [1,2] # Lead month(s)/ extension of forecast from start month e.g. 1 or 2 month forecast
forecasts = ['','weatherlogisticsltd'] # '' C3S multi-model mean, or 'weatherlogisticsltd' statistical, or '','weatherlogisticsltd' combined
moist_factor = 1.00 # 0% moistening due to regional climate change during winter season

for lead_time in lead_times:
    
    for mth_index, start_month in enumerate(start_months):

        lead_month = (int(start_month)+lead_time-1) % 12
        if lead_month < int(start_month):
            year_lead = int(start_years[mth_index]) + 1
        else:
            year_lead = int(start_years[mth_index])
        month_long = calendar.month_name[lead_month+1]
        print(month_long)
        
        now = datetime.datetime.now()
        copy_yr = now.year
        
        '''User to define 2 ascii plots to be compared'''
        ascii_files = []
        for forecast in forecasts:
            ascii_files.append(f'raw_data/ReClimate_{start_month}_{start_years[mth_index]}_{lead_time}{forecast}.asc')
        #
        title = (f'% Precipitation Compared to Recent Climate Mean\n{month_long} {year_lead}')
        variable_units = "Precipitation/ % of Climate"
        
        plt.figure(dpi=350, figsize=(10, 10))
        ax = plt.axes(projection=ccrs.Mercator(), frameon=True)
        # ax.suptitle("Re-Climate® February Rainfall Forecast. Copyright "+str(copy_yr)+". All rights reserved.")
        
        # Read in Re-Climate data header data
        for ascii_file in ascii_files:
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
            data_arrayx = np.loadtxt(ascii_file, dtype=np.float, skiprows=6)
            
            # Set the nodata values to nan
            data_arrayx[data_arrayx == data_nodata] = np.nan
            
            # Collate into array
            if ascii_file == ascii_files[0]:
                data_array = data_arrayx
            else:
                data_array += data_arrayx
        
        # Divide by forecast length
        data_array /= len(ascii_files)
        # Multiply by moistening factor
        data_array *= moist_factor
        
        # Plot Re-Climate ASCII grid with colorbar
        ax.set_title(title)
        
        # Show a colorbar legend
        img_plot = ax.imshow(data_array, cmap='seismic_r', vmin=80, vmax=120, alpha=0.8)
        
        # Greyscale coverage for non-extreme values
        enhance_color = np.ma.masked_where(np.array(abs(data_array)-100) < 5 , data_array)
        img_plot2 = ax.imshow(enhance_color, cmap='seismic_r', vmin=80, vmax=120, alpha=0.9)
         
        ax.grid(True)
        
        # Place a colorbar next to the map
        plt.suptitle('RE-CLIMATE Seasonal Climate Forecast', y=1.05, fontsize=18)
        plt.colorbar(img_plot2,orientation="horizontal",ax=ax,
                    pad=0,
                    aspect=50)
        
        # Save
        if len(forecasts) == 1:
            plt.savefig(f'raw_data/ReClimate_{start_month}_{start_years[mth_index]}_{lead_time}{forecast}.png', dpi=150, bbox_inches='tight')
        else:
            plt.savefig(f'raw_data/ReClimate_{start_month}_{start_years[mth_index]}_{lead_time}COMBINED.png', dpi=150, bbox_inches='tight')
        # Show forecast plots
        plt.show()
            