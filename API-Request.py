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

    # Building Header for Authenticated User Request
    user_header = {'Authorization': 'Bearer ' + id_token}
    
    # Sending the POST Request and reading the Response received.    
    response = requests.post(URL, json=request_data, headers=user_header)
    
    # Returning the Response received from the Re-Climate API
    return f"{response.text}"

# Specifying the URL to access the Re-Climate API
URL = "https://re-climate-4un5g5jztq-nw.a.run.app"
# Calling the function 'make_authorized_get_request' and displaying the response
print(make_authorized_get_request(URL))
