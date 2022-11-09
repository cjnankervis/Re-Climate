########## Importing the required modules ##############
import concurrent.futures
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
country = 'Spain' # 'uk' or 'spain' or 'turkey'
Cities = "SPAIN_TownsCities.csv" # "UK_TownCities.csv" or "SPAIN_TownCities.csv" or "TURKEY_TownsCities.csv"
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

URL = "https://re-climate-4un5g5jztq-nw.a.run.app"
    
# Fetching the Authentication Request from Environment Variables
auth_req = google.auth.transport.requests.Request()
# Fetching the ID Token from the Authentication Request
id_token = google.oauth2.id_token.fetch_id_token(auth_req, URL)

# Building Header for Authenticated User Request
user_header = {'Authorization': 'Bearer ' + id_token}

def load_url(URL, request_data, user_header, timeout):
    # Sending the POST Request and reading the Response received.    
    response = requests.post(URL, json=request_data, headers=user_header)
    return response

with concurrent.futures.ThreadPoolExecutor(max_workers=connections) as executor:
    
    # Extracting the User ID and User Email and storing in dictionary
    user_data = { "client_id" : f"{user_credentials['client_id']}", "client_email" : f"{user_credentials['client_email']}" }
    # Extracting the climate data from JSON file and storing in dictionary
    climate_data = []; request_data = []; request = []; future_to_url = []
    for n in range(num_cities):
        climate_data.append(json.load(open(climate_info_path)))
        
        # Adjust Re-Climate JSON information to read data from different town/ city locations
        climate_data[n]['country'] = country
        climate_data[n]['latitude'] = Cities_list.iloc[n][1]
        climate_data[n]['longitude'] = Cities_list.iloc[n][2]
    
        # Combining all the required data into single dictionary
        request_data.append(user_data | climate_data[n])
        
        request.append(load_url(URL, request_data[n], user_header, timeout))
    
        future_to_url.append(executor.submit(load_url, URL, request[n], user_header, timeout))
    
    out = []
    for future in concurrent.futures.as_completed(future_to_url):
        try:
            data = future.result()
        except Exception as exc:
            data = str(type(exc))
        finally:
            out.append(data)
            print(data)
