#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Wed Nov  9 17:00:32 2022
@author: Dr Christopher Nankervis, WeatherLogistics.
Re-Climate® Product Developer & Owner.
Description.
Allows multiple Re-Climate® API requests for a set of town/ city locations within a country bounding box

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
# Define the locations for the specified country
country = 'uk' # 'uk' or 'spain' or 'turkey'
Cities = "UK_TownsCities.csv" # "UK_TownCities.csv" or "SPAIN_TownCities.csv" or "TURKEY_TownsCities.csv"
Cities_list = pd.read_csv(Cities, header=None)

outputs = [] # Outputs are concatenated into a list
connections = 100 # Maximum number of concurrent requests
timeout = 60 # Request should take no longer than 1 minute per request

# Specifying the Service Account Credentials created for the User.
credential_path = "./User_Cred.json"
# Specifying the Climate info path
climate_info_path = "./Climate_Info.json"
###

# Determine the number of rows in the Cities location input file
num_cities = len(Cities_list)
# Loading the User  Credentials as Environment Variables
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
# Loading User Credentials from JSON file and storing in dictionary
user_credentials = json.load(open(credential_path))

# Endpoints. Specifying the URL to access the Re-Climate APIs
URL = "https://re-climatehistories-k7c6vv6pla-nw.a.run.app # Re-Climate Histories (supplies access to pre-2023 reforecasts)
# URL = "https://re-climate-4un5g5jztq-nw.a.run.app" # Re-Climate Standard Subscription (supplies access to town/ city data)
# URL = "https://re-climategauges-tynkl6dcla-nw.a.run.app" # Re-Climate Gauges (supplies access to English rainfall gauge data)
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
        
