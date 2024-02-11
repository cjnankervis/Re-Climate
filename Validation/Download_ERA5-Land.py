#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 21:47:52 2024

@author: Chris Nankervis, WeatherLogistics/ Re-Climate Trademark.
All rights reserved.

Download monthly ERA5-Land data for the United Kingdom

"""

import os
import numpy as np
import cdsapi

# User Inputs
download_singleyear = False; download_climate = True
country = 'UK' # Country's ERA5-land data to download ('UK', 'SPAIN', or 'TURKEY')
year = 2022 # Year to download
month_choices = np.array([1,2,3,4,11,12]) # Numerical month to download
###

month_nums = np.arange(1, 12+1)
months = [format('%02d' % month) for month in month_nums]
month_names = np.array(['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
    
BOUNDING_BOX = {'UK': (60.85, 2.69, 49.84, -10.7),
                'SPAIN': (44.17, 3.67, 35.71, -9.67), 
                'TURKEY': (42.14, 44.79, 35.82, 26.04)}
coords = BOUNDING_BOX[country]

c = cdsapi.Client()

for month_choice in month_choices:
    
    month = months[month_choice-1]
    month_name = month_names[month_choice-1]
    
    if download_singleyear:
        monthly_precip = 'ERA5-Land-'+month_name+str(year)+'.grib'
        if not os.path.exists('./ERA5/'+monthly_precip):
            # 1. Download monthly mean for the forecast analysis month
            c.retrieve(
                'reanalysis-era5-land-monthly-means',
                {
                    'product_type': 'monthly_averaged_reanalysis',
                    'variable': 'total_precipitation',
                    'year': str(year),
                    'month': month,
                    'time': '00:00',
                    'area': [
                        coords[0], coords[3], coords[2], coords[1],
                    ],
                    'format': 'grib',
                },
                monthly_precip)
    
    if download_climate:
        monthly_precip_climate = 'ERA5-Land-'+month_name+str(year)+'_Prev30Yrs.grib'
        if not os.path.exists('./ERA5/'+monthly_precip_climate):
            # 2. Download monthly means for the previous 30 years to generate a climatology
            c.retrieve(
                'reanalysis-era5-land-monthly-means',
                {
                    'product_type': 'monthly_averaged_reanalysis',
                    'variable': 'total_precipitation',
                    'year': ['1993', '1994', '1995', '1996',
                            '1997', '1998', '1999',
                            '2000', '2001', '2002',
                            '2003', '2004', '2005',
                            '2006', '2007', '2008',
                            '2009', '2010', '2011',
                            '2012', '2013', '2014',
                            '2015', '2016', '2017',
                            '2018', '2019', '2020',
                            '2021', '2022',],
                    'month': month,
                    'time': '00:00',
                    'area': [
                        coords[0], coords[3], coords[2], coords[1],
                    ],
                    'format': 'grib',
                },
                monthly_precip_climate)
