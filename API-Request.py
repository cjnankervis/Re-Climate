#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 10:08:00 2022

@author: WeatherLogistics/ Re-Climate® Product Developer & Owner.

Description.
API request script using authentication "key" provided
"""

import requests
import google.auth.transport.requests
import google.oauth2.id_token
import os
import json

def make_authorized_get_request(endpoint, audience):
    """
    Makes a request to the Re-Climate® HTTP endpoint by authenticating with the ID token.
    """
    # Specifying the Service Account Credentials created for the User.
    credential_path = "User.json"
    # Loading the Service Account Credentials as Environment Variables
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
    
    # Fetching the Authentication Request
    auth_req = google.auth.transport.requests.Request()
    # Fetching the ID Token from the Authentication Request
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)

    # Specifying the request to be sent
    with open('Climate_Info.json') as json_file:
        values = json.load(json_file)
    
    # Building Authenticated User Request
    user_header = {'Authorization': 'Bearer ' + id_token}
    
    response = requests.post(audience, json=values, headers=user_header)
    print(f"Response: {response.text}")


audience = endpoint = "https://europe-west2-calcium-pod-337210.cloudfunctions.net/ReClimate"

make_authorized_get_request(audience, endpoint)
