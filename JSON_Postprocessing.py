#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 16:05:09 2022

@author: Dr Christopher Nankervis, WeatherLogistics.
Re-Climate® Product Developer & Owner.

Description.
Post-processing code to generate climate hazard metrics.

Firstly 'ensemble' forecast data must be requested from the Re-Climate® API, which requires authorization.
Please contact the product owner (accounts@weatherlogistics.com).

Predicting the daily weather events more than 7-10 days in advance is challenging, and is non-deterministic i.e., there are a range of possible outcomes.
Each ensemble member provides a plausible future weather outcome, which provide a well-calibrated confidence interval (error bar) in the weather conditions. Together these comprise an ensemble.
In combination an ensemble provides a probabilistic viewpoint on the future likelihoods of events of different intensities.

The script below provides a quickstart framework to calculate frequencies of occurrence, daily counts, 
threshold or centile-based exceedance calculations, accumulations and consecutive days of events within specified thresholds.

The Python script is designed for use with daily weather inputs in a JSON format.

"""

# import pandas module 
import sys
import numpy as np
import pandas as pd
import json
from itertools import accumulate
from collections import Counter

'''User Inputs'''
filename = './OxfordWeatherLogisticsLtd_RainfallDAILYENSEMBLE-Mid-Winter2023_2023dClimate.json'
forecast_type = 'c3s' # 'c3s', 'wl', 'combined'
metric_type = 'centile' # 'days, 'frequency', 'accumulation', 'centile', 'consecutive'
threshold_type = 'above' # 'below', 'above', 'between' or ({threshold_type}, percentile) to assess consecutive days at a percentile level
thresholds = 97 # Single threshold value for daily weather event, or percentile if {metric_type} = 'centile'
forecast_month = (1) # 1,2 or 3 or any combination of month :: forecast month at t + {forecast_month}
units = 'degC' # Set the units for the output summaries (e.g. degC, mm)
###

month_names = ('January','February','March',\
               'April','May','June',\
               'July','August','September',\
               'October','November','December')
#
forecast_months = ((1,2,3),(2,3,4),(3,4,5),\
                   (4,5,6),(5,6,7),(6,7,8),\
                   (7,8,9),(8,9,10),(9,10,11),\
                   (10,11,12),(11,12,1),(12,1,2)) 

if metric_type == 'consecutive':
    '''Define the threshold_type and percentile for consecutive daily events'''
    if len(np.shape(threshold_type)):
        if len(threshold_type) == 2:
            try:
                percentile = threshold_type[1]; threshold_type = threshold_type[0]
            except TypeError:
                pass
        else:
            threshold_type = threshold_type[0]; percentile = 50
    else:
        threshold_type = threshold_type; percentile = 50 # Assess the median interval of consecutive days as a default
    
if threshold_type == 'between':
    '''Define the lower and upper threshold values for daily weather events'''
    try:
        threshold_lower = thresholds[0]; threshold_upper = thresholds[1]
    except TypeError:
        print('Error. Expecting two threshold values.')
        sys.exit()
    else:
        if len(thresholds) == 2:
            if thresholds[1] < thresholds[0]:
                print('Error. Threshold value 1 is less than value 0.')
                sys.exit()
        else:
            print('Error. Expecting two threshold values.')
            sys.exit()
else:
    if not len(np.shape(thresholds)):
        threshold = thresholds
    else:
        print('Error. Expecting one threshold value, but received multiple values.')
        sys.exit()

if not len(np.shape(forecast_month)):
    forecast_month = [forecast_month]

DailyEnsembleJSON = f'{filename}'

'''Read daily JSON outputs into a dataframe'''
with open(DailyEnsembleJSON, 'r') as f:
    data = json.load(f)
df_json = pd.DataFrame(data)['data']
dates = df_json.columns # datecode format 'dd/mm/yyyy'
datecodes = pd.to_datetime(dates, format="%d/%m/%Y"); date_list = np.array(dates)
indices = np.arange(0,len(date_list))
first_month = date_list[0][3:5] # Establish the first forecast month
#
if len(np.shape(forecast_month)):
    month_name = [month_names[forecast_months[int(first_month)-1][m-1]-1] for m in forecast_month]
else:
    month_name = [month_names[forecast_months[int(first_month)-1][forecast_month[0]-1]-1]]
#
month2 = format('%02d' % forecast_months[int(first_month)-1][1]) # Second forecast month
month3 = format('%02d' % forecast_months[int(first_month)-1][2]) # Third forecast month
#
mth1_idx = indices[datecodes.strftime('%m')==first_month]
mth2_idx = indices[datecodes.strftime('%m')==month2]
mth3_idx = indices[datecodes.strftime('%m')==month3]

data_array = np.array(df_json['data'])
if forecast_type.lower() == 'wl':
    '''Model type 1. WeatherLogistics Statistical Forecast System'''
    df_subset = [data_array[0:50,mth1_idx], data_array[0:50,mth2_idx], data_array[0:50,mth3_idx]]
    num_ensembles = 50
elif forecast_type.lower() == 'c3s':
    '''Model type 2. Copernicus Climate Change Service Multi-Model Average.'''
    df_subset = [data_array[50:100,mth1_idx], data_array[50:100,mth2_idx], data_array[50:100,mth3_idx]]
    num_ensembles = 50
elif forecast_type.lower() == 'combined':
    '''Model type 3. Combined WeatherLogistics and Copernicus Climate Change Service Multi-Model Average.'''
    df_subset = [data_array[0:100,mth1_idx], data_array[0:100,mth2_idx], data_array[0:100,mth3_idx]]
    num_ensembles = 100

'''Compute meteorological statistics'''
for m_ind, m in enumerate(forecast_month):
    if not m_ind:
        mth_data = df_subset[m-1]; mth_days = np.shape(df_subset[m-1])[1]
    else:
        mth_data = np.concatenate((mth_data, df_subset[m-1]), axis=1); mth_days += np.shape(df_subset[m-1])[1]

if threshold_type.lower() == 'above':
    '''Predicted number of days with event intensities equal to or above a threshold'''
    if metric_type.lower() == 'days':
        '''Count of meteorological events equal to or above a threshold value'''
        metric_description = f'Count of meteorological events equal to or above {threshold}{units}'
        metric_output = round(sum(mth_data.flatten() >= threshold) / num_ensembles, 2)
    elif metric_type.lower() == 'frequency':
        '''Probability of event with intensities equal to or above threshold'''
        metric_description = f'Probability of event with intensities equal to or above {threshold}{units}'
        metric_output = round(sum(mth_data.flatten() >= threshold) / (num_ensembles * mth_days), 2)
    elif metric_type.lower() == 'accumulation':
        '''Accumulated meteorological value of daily event with an intensity equal to or above threshold'''
        metric_description = f'Accumulated meteorological value of daily event with an intensity equal to or above {threshold}{units}'
        metric_output = round(np.mean([sum(mth_data[e][mth_data[e] >= threshold]) for e in range(num_ensembles)]) / num_ensembles * mth_days, 2)
    elif metric_type.lower() == 'centile':
        '''Average intensity of daily events with a probability threshold equal to or above a centile threshold'''
        metric_description = f'Average intensity of daily events with a probability threshold equal to or above {threshold}th centile'
        metric_output = round(np.mean([sum(mth_data[e][mth_data[e] >= np.percentile(mth_data[e], threshold)]) for e in range(num_ensembles)]), 2)
    elif metric_type.lower() == 'consecutive':
        '''Mean consecutive days with an event intensity equal to or above a threshold'''
        metric_description = f'Mean consecutive days with an event intensity equal to or above {threshold}{units}'
        counts_list = []
        for e in range(num_ensembles):
            groups = accumulate([0]+[(a>=threshold) != (b>=threshold) for a,b in zip(mth_data[e],mth_data[e][1:])])
            counts = sorted(Counter(groups).items())
            groups2 = [c for n,c in counts if (n%2==0) == (mth_data[e][0]>=threshold)]
            groups2 = [0] if not groups2 else groups2 # Weight by ensemble size, to take into account ensemble members with zero consecutive days
            counts_list.append(groups2)
        flat_list = [item for sublist in counts_list for item in sublist]
        metric_output = np.nanpercentile(flat_list, (1-1/(num_ensembles*percentile/100*2))*100)
        metric_output = round(np.mean(metric_output), 2) if np.isfinite(np.nanmean(metric_output)) else 0.0

if threshold_type.lower() == 'below':
    '''Predicted number of days with event intensities equal to or below a threshold'''
    if metric_type.lower() == 'days':
        '''Count of meteorological events equal to or below a threshold value'''
        metric_description = f'Count of meteorological events equal to or below {threshold}{units}'
        metric_output = round(sum(mth_data.flatten() <= threshold) / num_ensembles, 2)
    elif metric_type.lower() == 'frequency':
        '''Probability of event with intensities equal to or below threshold'''
        metric_description = f'Probability of event with an intensity below {threshold}{units}'
        metric_output = round(sum(mth_data.flatten() <= threshold) / (num_ensembles * mth_days), 2)
    elif metric_type.lower() == 'accumulation':
        '''Accumulated meteorological value of daily event with an intensity equal to or below {threshold}{units} threshold'''
        metric_description = f'Accumulated meteorological value of daily event with an intensity equal to or below {threshold}{units}'
        metric_output = round(np.mean([sum(mth_data[e][mth_data[e] <= threshold]) for e in range(num_ensembles)]) / num_ensembles * mth_days, 2)
    elif metric_type.lower() == 'centile':
        '''Average intensity of daily event with a probability threshold equal to or below a centile threshold'''
        metric_description = f'Average intensity of daily event with a probability threshold equal to or below {threshold}th centile'
        metric_output = round(np.mean([sum(mth_data[e][mth_data[e] <= np.percentile(mth_data[e], threshold)]) for e in range(num_ensembles)]), 2)
    elif metric_type.lower() == 'consecutive':
        '''Mean consecutive days with an events intensity equal to or below a threshold'''
        metric_description = f'Mean consecutive days with an event intensity equal to or below {threshold}{units}'
        counts_list = []
        for e in range(num_ensembles):
            groups = accumulate([0]+[(a<=threshold) != (b<=threshold) for a,b in zip(mth_data[e],mth_data[e][1:])])
            counts = sorted(Counter(groups).items())
            groups2 = [c for n,c in counts if (n%2==0) == (mth_data[e][0]<=threshold)]
            groups2 = [0] if not groups2 else groups2 # Weight by ensemble size, to take into account ensemble members with zero consecutive days
            counts_list.append(groups2)
        flat_list = [item for sublist in counts_list for item in sublist]
        metric_output = np.nanpercentile(flat_list, (1-1/(num_ensembles*percentile/100*2))*100)
        metric_output = round(np.mean(metric_output), 2) if np.isfinite(np.nanmean(metric_output)) else 0.0

if threshold_type.lower() == 'between':
    '''Predicted number of days with event intensities between a lower and upper threshold'''
    if metric_type.lower() == 'days':
        '''Count of meteorological events between a lower and upper threshold'''
        metric_description = f'Count of meteorological events between {threshold_lower}{units} and {threshold_upper}{units}'
        metric_output = round(sum((mth_data.flatten() >= threshold_lower) & (mth_data.flatten() <= threshold_upper)) / num_ensembles, 2)
    elif metric_type.lower() == 'frequency':
        '''Probability of event with intensities between thresholds'''
        metric_description = f'Probability of event with intensities between {threshold_lower}{units} and {threshold_upper}{units}'
        metric_output = round(sum((mth_data.flatten() >= threshold_lower) & (mth_data.flatten() <= threshold_upper)) / (num_ensembles * mth_days), 2)
    elif metric_type.lower() == 'accumulation':
        '''Accumulated meteorological value of daily events with an intensity between thresholds'''
        metric_description = f'Accumulated meteorological value of daily event with intensities between {threshold_lower}{units} and {threshold_upper}{units}'
        metric_output = round(np.mean([sum(mth_data[e][(mth_data[e] >= threshold_lower) & (mth_data[e] <= threshold_upper)]) for e in range(num_ensembles)]) / num_ensembles * mth_days, 2)
    elif metric_type.lower() == 'centile':
        '''Average intensity of daily event with a probability threshold between a lower and upper centile threshold'''
        metric_description = f'Average intensity of daily events with a probability threshold between {threshold_lower}th and {threshold_upper}th centiles'
        metric_output = round(np.mean([sum(mth_data[e][(mth_data[e] >= np.percentile(mth_data[e], threshold_lower)) & (mth_data[e] <= np.percentile(mth_data[e], threshold_upper))]) for e in range(num_ensembles)]), 2)
    elif metric_type.lower() == 'consecutive':
        '''Mean consecutive days with an event intensity between a lower and upper threshold'''
        metric_description = f'Mean consecutive days with event intensities between {threshold_lower}{units} and {threshold_upper}{units}'
        counts_list = []
        for e in range(num_ensembles):
            groups = accumulate([0]+[((a>=threshold_lower) & (a>=threshold_upper)) != ((b<threshold_lower) & (b>threshold_upper)) for a,b in zip(mth_data[e],mth_data[e][1:])])
            counts = sorted(Counter(groups).items())
            groups = [c for n,c in counts if (n%2==0) == ((mth_data[e][0]>=threshold_lower) & (mth_data[e][0]<=threshold_upper))]
            groups = [0] if not groups else groups # Weight by ensemble size, to take into account ensemble members with zero consecutive days
            counts_list.append(groups2)
        flat_list = [item for sublist in counts_list for item in sublist]
        metric_output = np.nanpercentile(flat_list, (1-1/(num_ensembles*percentile/100*2))*100)
        metric_output = round(np.mean(metric_output), 2) if np.isfinite(np.nanmean(metric_output)) else 0.0

print(f"{metric_description} is {metric_output}, which is based on analysis of {num_ensembles} ensemble members and {mth_days} days in {', '.join(month_name)}")
