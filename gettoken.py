import base64
from dotenv import load_dotenv
import os
from requests import post, get
import json
import requests
import spotipy

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
scope = "user-read-playback-state"  
redirect_uri = 'http://127.0.0.1:5500/callback'
auth_url = 'https://accounts.spotify.com/authorize'

auth_params = {
    'client_id': client_id,
    'response_type': 'code',
    'redirect_uri': redirect_uri,
    'scope': scope,
}

authorization_url = auth_url + '?' + '&'.join([f'{key}={value}' for key, value in auth_params.items()])
print("Please visit the following URL in your browser to authorize the application:")
print(authorization_url)

# Prompt the user to enter the authorization code from the redirected URL
authorization_code = input("Enter the authorization code from the redirected URL: ")

# Step 2: Exchange Authorization Code for Token
token_url = 'https://accounts.spotify.com/api/token'

token_params = {
    'grant_type': 'authorization_code',
    'code': authorization_code,
    'redirect_uri': redirect_uri,
    'client_id': client_id,
    'client_secret': client_secret,
}

token_response = requests.post(token_url, data=token_params)

# The response contains the access token, refresh token, and other information
token_data = token_response.json()

access_token = token_data.get('access_token')
refresh_token = token_data.get('refresh_token')
expires_in = token_data.get('expires_in')

print("Access Token:", access_token)
print("Refresh Token:", refresh_token)
print("Expires In:", expires_in)

