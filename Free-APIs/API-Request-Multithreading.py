#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thurs Jun  29 10:22:25 2023

@author: Dr Christopher Nankervis, WeatherLogistics.
Re-Climate® Product Developer & Owner.

Description.
For a single Re-Climate® API location request within a country bounding box/

'forecast-histories': UK, Spain and Turkey mainland. Seasonal climate forecasts (for the next 3 calendar months), 
as issued from March 2023 to June 2023 inclusive.

'forecastgauges-histories': English precipitation data only. Seasonal climate forecasts (for the next 3 calendar months), 
as issued from March 2023 to June 2023 inclusive.

'rcp-standard': UK only. Representative Concentration Pathways (RCPs) 2.6 and 8.5, based on UK Climate Projection Data 2018.
Projections are available for the seasons spring, summer, autumn and winter - and for the years 2025, 2035 and 2045.

'rcp-gauges': English precipitation data only. Representative Concentration Pathways (RCPs) 2.6 and 8.5, based on UK Climate Projection Data 2018.
Projections are available for the seasons spring, summer, autumn and winter - and for the years 2025, 2035 and 2045.

Further Information,
    See https://github.com/cjnankervis/Re-Climate/
    
Contact.
    Dr Christopher Nankervis,
    Email. accounts@weatherlogistics.com

"""

########## Importing the required modules ##############
from concurrent.futures import ThreadPoolExecutor, as_completed
# Import Pandas
import pandas as pd
# Importing Requests module
import requests
# Importing Google Auth Modules
import google.auth.transport.requests
import google.oauth2.id_token
# Importing Os Module
import os
# Importing JSON Module
import json

'''User Inputs'''
API_CHOICE = 'forecastgauges-histories' # 'rcp-standard' OR 'rcp-gauges' OR 'forecast-histories' OR 'forecastgauges-histories'
###
# Define the locations for the specified country
country = 'uk' # 'uk' or 'spain' or 'turkey'
Cities = "UK_TownsCities.csv" # "UK_TownCities.csv" or "SPAIN_TownCities.csv" or "TURKEY_TownsCities.csv"
Cities_list = pd.read_csv(Cities, header=None)

outputs = [] # Outputs are concatenated into a list
connections = 100 # Maximum number of concurrent requests
timeout = 60 # Request should take no longer than 1 minute per request

# Specifying the appropriate Google Cloud Service Account Credentials:
if API_CHOICE.lower() in ('rcp-standard', 'rcp-gauges'):
    credential_path = './User_Credentials-rcps.json'
    # Specifying the Climate info path
    if API_CHOICE.lower() == 'rcp-standard':
        climate_info_path = './Climate_Info-rcps.json'
    elif API_CHOICE.lower() == 'rcp-gauges':
        climate_info_path = './Climate_Info-rcpgauges.json'
elif API_CHOICE.lower() in ('forecast-histories', 'forecastgauges-histories'):
    credential_path = './User_Credentials-forecasts.json'
    # Specifying the Climate info path
    if API_CHOICE.lower() == 'forecast-histories':
        climate_info_path = './Climate_Info-forecasts.json'
    elif API_CHOICE.lower() == 'forecastgauges-histories':
        climate_info_path = './Climate_Info-forecastsgauges.json'
print(f'Reading API credentials from {credential_path} and inputs from {climate_info_path}')
###

# Determine the number of rows in the Cities location input file
num_cities = len(Cities_list)
# Loading the User  Credentials as Environment Variables
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
# Loading User Credentials from JSON file and storing in dictionary
user_credentials = json.load(open(credential_path))

# Endpoints. Specifying the URL to access the Re-Climate APIs
# Specifying the URL to access the Re-Climate API
'''Climate Projections for United Kingdom Town/ Cities or closest match'''
if API_CHOICE.lower() == 'rcp-standard':
    URL = "https://europe-west2-weatherdocker-standardrcp.cloudfunctions.net/re-climateRCP"
elif API_CHOICE.lower() == 'rcp-gauges':
    '''Climate Projections at English EA (gov.uk) Rainfall Tipping Point Gauges'''
    URL = "https://europe-west2-weatherdocker-standardrcp.cloudfunctions.net/re-climateRCPGAUGES"
elif API_CHOICE.lower() == 'forecast-histories':
    URL = "https://re-climatehistories-k7c6vv6pla-nw.a.run.app"
elif API_CHOICE.lower() == 'forecastgauges-histories':
    URL = "https://europe-west2-weatherdocker-histories.cloudfunctions.net/forecast-gaugeshistories"
# Calling the function 'make_authorized_get_request' and displaying the response
    
# Fetching the Authentication Request from Environment Variables
auth_req = google.auth.transport.requests.Request()
# Fetching the ID Token from the Authentication Request
id_token = google.oauth2.id_token.fetch_id_token(auth_req, URL)

# Building Header for Authenticated User Request
user_header = {"Content-Type": "application/json", "Authorization": "Bearer " + id_token}

def load_url(URL, request_data, user_header):
    # Sending the POST Request and reading the Response received.
    response = requests.post(URL, json=request_data, headers=user_header, stream=True)
    
    try:
        request_data["filename"]
    except KeyError:
        request_data["filename"] = None
    
    if request_data["extension"] == 'png' or request_data["filename"]:
        if request_data["filename"]:
            if response.status_code == 200:
                with open(request_data["filename"], 'wb') as f:
                    for chunk in response:
                        f.write(chunk)
                    print(f'Hazard index file was saved to {request_data["filename"]}')
                f.close()
        else:
            with open("output.png", 'wb') as f:
                for chunk in response:
                    f.write(chunk)
                print('Hazard index file was saved to output.png')
            f.close()
    else:
        if request_data["extension"] == 'csv':
            response = response.text
        else:
            try:
                response = response.json().replace("\'", "\"")
            except Exception as e:
                try:
                    response = response.text.replace("\'", "\"")
                except Exception as e:
                    print(e)
                    pass
        print(response)
    #
    return response
    
# Extracting the User ID and User Email and storing in dictionary
user_data = { "client_id" : f"{user_credentials['client_id']}", "client_email" : f"{user_credentials['client_email']}" }
# Extracting the climate data from JSON file and storing in dictionary
climate_data = []; request_data = []; response = []; data = []
with ThreadPoolExecutor(max_workers=200) as executor:
    for n in range(num_cities):
        climate_data.append(json.load(open(climate_info_path)))
        
        # Adjust Re-Climate JSON information to read data from different town/ city locations
        climate_data[n]['country'] = str(country)
        climate_data[n]['latitude'] = Cities_list.iloc[n][1]
        climate_data[n]['longitude'] = Cities_list.iloc[n][2]
    
        # Combining all the required data into single dictionary
        request_data.append(user_data | climate_data[n])
        
        response.append(load_url(URL, request_data[n], user_header))
        print(f"{response[n]}")
        
        '''N.b. Column/ item length of 100 indicates Ensemble Numbers from 1 to 100'''
        
        # Write API string data to an output
        data.append(response[n])
        