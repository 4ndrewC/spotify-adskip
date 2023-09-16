from flask import Flask, request, redirect
import requests
import requests
import base64
import time
import subprocess
import os
import pyautogui as pg
import webbrowser


app = Flask(__name__)

#api params
CLIENT_ID = "d3d46d184b734ccb8b70003dcc7ca687"
CLIENT_SECRET = "d11522290886440b8b13fc4aef532bb9"
REDIRECT_URI = 'http://127.0.0.1:5500/callback'
SCOPE = 'user-read-playback-state' 

AUTH_URL = f'https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'

def open_spotify(command):
    subprocess.Popen(["nircmd.exe", "exec", "hide", command])


def close_spotify():
    os.system("taskkill /im Spotify.exe")

def play():
    pg.press('playpause')

spotify_command = "C:\\Users\\Andrew\\AppData\\Roaming\\Spotify\\Spotify.exe"

def get_current_track(access_token):
  while(True):
    # time.sleep(1)
    # print('yes')
    try:
        response = requests.get(CURRENT_TRACK_URL,
                          headers={"Authorization": f"Bearer {access_token}"})
        if response.status_code==200:
            # json_resp = response.json()
            current_track_info = response.json()
            name = ""
            type = current_track_info['currently_playing_type']
            if type=='ad':
                name = "ad"
                
            elif type=='track':
                name = current_track_info['item']['name']

            if len(songs)==0 or (len(songs)>0 and songs[-1]!=name):
                print('name: ', name, '\n' + 'type: ', type)
                songs.append(name)
            
            if type=='ad':
                close_spotify()
                time.sleep(1)
                open_spotify(spotify_command)
                time.sleep(1)
                play()
        elif response.status_code==401:
            return -1
            
    except:
        print('somethign worng')
    time.sleep(1)

@app.route('/start_auth')
def start_auth():
    return redirect(AUTH_URL)

songs = []
@app.route('/callback')
def callback():
    # print('args: ', request.args)
    authorization_code = request.args.get('code')
    
    if authorization_code:
        #get auth token from auth code
        token_params = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': REDIRECT_URI,
        }
        headers = {
            'Authorization': f'Basic {base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()}',
        }
        token_response = requests.post(TOKEN_URL, data=token_params, headers=headers)
        token_data = token_response.json()
        access_token = token_data.get('access_token')

        if access_token:
            run = get_current_track(access_token)
            if run == -1:
                redirect('/start_auth')
        else:
            return 'Access token not obtained.'
    return 'Authorization code not received.'

webbrowser.open('http://127.0.0.1:5500/start_auth')

if __name__ == '__main__':
    app.run(debug=True, port=5500)