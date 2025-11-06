import spotipy
from spotipy.oauth2 import SpotifyOAuth

from load_data import load_songs

import os 
from dotenv import load_dotenv

import csv 

load_dotenv()

load_songs()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://127.0.0.1:8888",
        scope="user-library-read user-library-modify",
    )
)

album_info = {}

with open("liked_songs.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
        track_name = row[0]
        artist = row[1]
        album_name = row[2]
        track_id = row[3]
        album_id = row[4]
        album_type = row[5]
        total_tracks = int(row[6])

        if album_id not in album_info:
            album_info[album_id] = {
                "name": album_name,
                "artist": artist,
                "total_tracks": total_tracks,
                "type": album_type
            }

albums_to_add = list(album_info.keys())

for i, album_id in enumerate(albums_to_add):
    info = album_info[album_id]
    type = info["type"]

for i in range(0, len(albums_to_add), 50):
    batch = albums_to_add[i: i + 50]
    sp.current_user_saved_albums_add(batch)
    print(f"Progress: {min(i+50, len(albums_to_add))}/{len(albums_to_add)}")
