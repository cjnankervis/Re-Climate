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
Projections are available for the summer season ONLY - and for the years 2025, 2035 and 2045.

Further Information,
    See https://github.com/cjnankervis/Re-Climate/
    
Contact.
    Dr Christopher Nankervis,
    Email. accounts@weatherlogistics.com

"""

########## Importing the required modules ##############
# Importing Requests module
import requests
# Importing Google Auth Modules
import google.auth.transport.requests
import google.oauth2.id_token
# Importing Os Module
import os
# Importing JSON Module
import json

'''USER SPECIFICATION: Re-Climate API type'''
API_CHOICE = 'forecastgauges-histories' # 'rcp-standard' OR 'rcp-gauges' OR 'forecast-histories' OR 'forecastgauges-histories'
###

# Defining Function to send Authorised Requests.
def make_authorized_get_request(URL):
    """
    make_authorized_get_request send a POST request to the specified HTTP(S) endpoint
    by authenticating with the ID token obtained from the google-auth client library
    using the specified URL.
    """
    
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

    # Extracting the climate data from JSON file and storing in dictionary
    climate_data = json.load(open(climate_info_path))
    
    # Loading the User  Credentials as Environment Variables
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
    # Loading User Credentials from JSON file and storing in dictionary
    user_credentials = json.load(open(credential_path))
        
    # Fetching the Authentication Request from Environment Variables
    auth_req = google.auth.transport.requests.Request()
    # Fetching the ID Token from the Authentication Request
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, URL)

    # Extracting the User ID and User Email and storing in dictionary
    user_data = { "client_id" : f"{user_credentials['client_id']}", "client_email" : f"{user_credentials['client_email']}" }
    
    # Combining all the required data into single dictionary
    request_data = user_data | climate_data
    
    try:
        climate_data["filename"]
    except KeyError:
        climate_data["filename"] = None

    # Building Header for Authenticated User Request
    user_header = {"Content-Type": "application/json", "Authorization": "Bearer " + id_token}
    
    # Sending the POST Request and reading the Response received.    
    response = requests.post(URL, json=request_data, headers=user_header, stream=True)
    print(response.text)

    '''N.b. Column/ item length of 100 indicates Ensemble Numbers from 1 to 100'''
    if climate_data["extension"] == 'png' or climate_data["filename"]:
        if climate_data["filename"]:
            if response.status_code == 200:
                with open(climate_data["filename"], 'wb') as f:
                    for chunk in response:
                        f.write(chunk)
                    print(f'Hazard index file was saved to {climate_data["filename"]}')
                f.close()
        else:
            with open("output.png", 'wb') as f:
                for chunk in response:
                    f.write(chunk)
                print('Hazard index file was saved to output.png')
            f.close()
    else:
        if climate_data["extension"] == 'csv':
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
    
    # Returning the Response received from the Re-Climate API
    return response

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
out = make_authorized_get_request(URL)
