#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Created on Wed Nov  9 17:01:25 2022
@author: Dr Christopher Nankervis, WeatherLogistics.
Re-Climate® Product Developer & Owner.

Description.
For a single Re-Climate® API location request for within a country bounding box

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

# Defining Function to send Authorised Requests.
def make_authorized_get_request(URL):
    """
    make_authorized_get_request send a POST request to the specified HTTP(S) endpoint
    by authenticating with the ID token obtained from the google-auth client library
    using the specified URL.
    """
    # Specifying the Service Account Credentials created for the User.
    credential_path = "./User_Cred.json"
    # Specifying the Climate info path
    climate_info_path = "./Climate_Info.json"
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

# Endpoints. Specifying the URL to access the Re-Climate APIs
URL = "https://re-climatehistories-k7c6vv6pla-nw.a.run.app # Re-Climate Histories (supplies access to pre-2023 reforecasts)
# URL = "https://re-climate-4un5g5jztq-nw.a.run.app" # Re-Climate Standard Subscription (supplies access to town/ city data)
# URL = "https://re-climategauges-tynkl6dcla-nw.a.run.app" # Re-Climate Gauges (supplies access to English rainfall gauge data)
# Calling the function 'make_authorized_get_request' and displaying the response
out = make_authorized_get_request(URL)
