#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Sat Jan 20 20:22:02 2024

@author: Dr Christopher Nankervis, WeatherLogistics.
Re-Climate® Product Developer & Owner.

Description.
Compares the country-wide plot of a Re-Climate® precipitation variables.

"""

import os
import numpy as np
import matplotlib.pyplot as plt
import datetime
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cf
import pandas as pd

country = 'UK' # Analysis data is currently available for the UK only
start_years = ['2023','2023','2023','2024','2024'] # Forecast initiation years ['2023','2023','2023','2024']
start_months = ['10','11','12','01','02'] # Forecast start/ valid month ['10','11','12','01']
lead_times = [1,2] # Lead month(s)/ extension of forecast from start month e.g. 1 or 2 month forecast
suppliers = ['ecmwf', 'ukmo', 'ncep'] # 'ecmwf' (sys 51), 'ukmo' (sys 602), 'ncep' (sys 2)

for supplier in suppliers:

    systems = {'ecmwf': 51,
               'ukmo': 602,
               'ncep': 2}
    
    BOUNDING_BOX = {'UK': (60.85, 2.69, 49.84, -10.7),
                    'SPAIN': (44.17, 3.67, 35.71, -9.67), 
                    'TURKEY': (42.14, 44.79, 35.82, 26.04)}
    
    for mth_index, start_month in enumerate(start_months):
    
        if not os.path.isfile(f'raw_data/comparison_{start_month}_{start_years[mth_index]}_{supplier}.grib'):
            import cdsapi
            c = cdsapi.Client()
            c.retrieve(
                'seasonal-postprocessed-single-levels',
                {
                    'format': 'grib',
                    'originating_centre': supplier,
                    'system': systems[supplier],
                    'variable': 'total_precipitation_anomalous_rate_of_accumulation',
                    'product_type': [
                        'ensemble_mean', 'monthly_mean',
                    ],
                    'year': start_years[mth_index],
                    'month': start_month,
                    'leadtime_month': [
                        '1', '2',
                    ],
                },
                f'raw_data/comparison_{start_month}_{start_years[mth_index]}_{supplier}.grib')
            
        ds = xr.open_dataset(
            f'raw_data/comparison_{start_month}_{start_years[mth_index]}_{supplier}.grib', 
            filter_by_keys={'dataType': 'em'}
            )
        
        for lead_time in lead_times:
        
            # We want forecast for month ahead, we chose first element of our dataset
            first_month = ds["tpara"][lead_time-1]
            # Transform 0 to 360 degree longitudes, to true longitude
            first_month["longitude"] = (first_month["longitude"] + 180) % 360 - 180
            first_month = first_month.sortby(first_month.longitude)
            # Create plot and set up basemap
            plt.figure(dpi=350, figsize=(10, 10))
            ax = plt.axes(projection=ccrs.Mercator(), frameon=True)
            # Set coordinate system of data and change extent of a map
            data_crs = ccrs.PlateCarree()
            coords = BOUNDING_BOX[country]
            ax.set_extent([coords[3], coords[1], coords[2], coords[0]], crs=data_crs)
            # Load values and latitude and longitude
            values = first_month.values
            ax.add_feature(cf.COASTLINE.with_scale("50m"), lw=0.5) # Add borderlines
            ax.add_feature(cf.BORDERS.with_scale("50m"), lw=0.3) # Add coastlines
            ax.add_feature(cf.OCEAN, zorder=100, edgecolor='k', color='#ffffff') # Mask out oceans
            lonsi, latsi = np.meshgrid(first_month["longitude"], first_month["latitude"]) # Create grid from latitude and longitude
            # Plot the data as filled contour
            vmin = -0.000000045; vmax = 0.000000045
            levels = np.linspace(vmin, vmax, 32+1)
            cs = ax.contourf(lonsi, latsi, values, transform=data_crs, levels=levels, cmap="seismic_r", vmin=vmin, vmax=vmax)
            # Get attributes needed for title
            name = first_month.attrs["GRIB_name"]
            units = first_month.attrs["GRIB_units"]
            valid_date = first_month.valid_time.values
            valid_date = pd.to_datetime(valid_date)
            valid_date = valid_date.strftime("%B %Y")
            plt.suptitle(supplier.upper()+', System '+str(systems[supplier]), y=1.05, fontsize=18)
            plt.title(f"{name}\n({units}) {valid_date}")
            plt.colorbar(cs,orientation="horizontal",ax=ax,
                        pad=0,
                        aspect=50)
            
            now = datetime.datetime.now()
            copy_yr = now.year
            
            # Save Plot
            plt.savefig(f'raw_data/comparison_{start_month}_{start_years[mth_index]}_{lead_time}_{supplier}.png', dpi=350, bbox_inches='tight')
    
