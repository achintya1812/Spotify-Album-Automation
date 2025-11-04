import spotipy
from spotipy.oauth2 import SpotifyOAuth

import os
from dotenv import load_dotenv

import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = client_id,
                                               client_secret = client_secret,
                                               redirect_uri = "http://127.0.0.1:8888",
                                               scope = "user-library-read"))

results = sp.current_user_saved_tracks()
tracks = results["items"]

while results["next"]:
    results = sp.next(results)
    tracks.extend(results["items"])

for index, item in enumerate(tracks):
    track = item["track"]
    print(index, track["artists"][0]["name"], " - ", track["name"])

with open("liked_songs.json", "w") as file:
    json.dump(tracks, file, indent = 2)
