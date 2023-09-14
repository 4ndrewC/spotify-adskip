import requests
import time
import pyautogui as pg

from pprint import pprint
import subprocess
import os

def open_spotify(command):
    subprocess.Popen(["nircmd.exe", "exec", "hide", command])


def close_spotify():
    os.system("taskkill /im Spotify.exe")

def play():
  pg.press('playpause')

#put your spotify directory for spotify_command
spotify_command = ""


SPOTIFY_GET_CURRENT_TRACK_URL = 'https://api.spotify.com/v1/me/player/currently-playing'
ACCESS_TOKEN = ""

def get_current_track(access_token):
  response = requests.get(SPOTIFY_GET_CURRENT_TRACK_URL,
                          headers={"Authorization": f"Bearer {access_token}"})
  json_resp = response.json()
  return json_resp


songs = []

def main():
  current_track_id = None
  while True:
    try:
      current_track_info = get_current_track(ACCESS_TOKEN)
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
    except:
       print('somethign worng')



if __name__ == '__main__':
  main()
