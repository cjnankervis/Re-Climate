#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Sat Jan 20 20:22:02 2024

@author: Dr Christopher Nankervis, WeatherLogistics.
Re-Climate® Product Developer & Owner.

Description.
Compares the country-wide plot of a Re-Climate® temperature variables.

"""

import os
import numpy as np
import matplotlib.pyplot as plt
import datetime
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cf
import pandas as pd

country = 'UK'
start_year = '2023'
start_months = ('10','11','12')
lead_times = (1, 2)
suppliers = ('ecmwf', 'ukmo', 'ncep') # 'ecmwf' (sys 51), 'ukmo' (sys 602), 'ncep' (sys 2)

for supplier in suppliers:

    systems = {'ecmwf': 51,
               'ukmo': 602,
               'ncep': 2}
    
    BOUNDING_BOX = {'UK': (60.85, 2.69, 49.84, -10.7),
                    'SPAIN': (44.17, 3.67, 35.71, -9.67), 
                    'TURKEY': (42.14, 44.79, 35.82, 26.04)}
    
    for start_month in start_months:
    
        if not os.path.isfile(f'raw_data/comparison_{start_month}_{start_year}_{supplier}_Temperature.grib'):
            import cdsapi
            c = cdsapi.Client()
            c.retrieve(
                'seasonal-postprocessed-single-levels',
                {
                    'format': 'grib',
                    'originating_centre': supplier,
                    'system': systems[supplier],
                    'variable': '2m_temperature_anomaly',
                    'product_type': [
                        'ensemble_mean', 'monthly_mean',
                    ],
                    'year': start_year,
                    'month': start_month,
                    'leadtime_month': [
                        '1', '2',
                    ],
                },
                f'raw_data/comparison_{start_month}_{start_year}_{supplier}_Temperature.grib')
            
        ds = xr.open_dataset(
            f'raw_data/comparison_{start_month}_{start_year}_{supplier}_Temperature.grib', 
            filter_by_keys={'dataType': 'em'}
            )
        
        for lead_time in lead_times:
        
            # We want forecast for month ahead, we chose first element of our dataset
            first_month = ds["t2m"][lead_time-1]
            # Transform 0 to 360 degree long          itudes, to longitude
            first_month["longitude"] = (first_month["longitude"] + 180) % 360 - 180
            first_month = first_month.sortby(first_month.longitude)
            # Create plot and set up basemap
            plt.figure(dpi=350)
            ax = plt.axes(projection=ccrs.Mercator(), frameon=True)
            # Set coordinate system of data and change extent of a map
            data_crs = ccrs.PlateCarree()
            coords = BOUNDING_BOX[country]
            ax.set_extent([coords[3], coords[1], coords[2], coords[0]], crs=data_crs)
            # Load values and latitude and longitude
            values = first_month.values
            ax.add_feature(cf.COASTLINE.with_scale("50m"), lw=0.5) # Add borderlines
            ax.add_feature(cf.BORDERS.with_scale("50m"), lw=0.3) # Add coastlines
            lonsi, latsi = np.meshgrid(first_month["longitude"], first_month["latitude"]) # Create grid from latitude and longitude
            # Plot the data as filled contour
            cs = ax.contourf(lonsi, latsi, values, transform=data_crs, levels=128, cmap="seismic_r", vmin=-0.000000045, vmax=0.000000045)
            # Get attributes needed for title
            name = first_month.attrs["GRIB_name"]
            units = first_month.attrs["GRIB_units"]
            valid_date = first_month.valid_time.values
            valid_date = pd.to_datetime(valid_date)
            valid_date = valid_date.strftime("%B %Y")
            plt.suptitle(supplier.upper(), y=1.05, fontsize=18)
            plt.title(f"{name} ({units}) {valid_date}")
            plt.colorbar(cs,orientation="horizontal",ax=ax,
                        pad=0,
                        aspect=50)
            
            # Save Plot
            plt.savefig(f'raw_data/comparison_{start_month}_{start_year}_{lead_time}_{supplier}_Temperature.png', dpi=350)
