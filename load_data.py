import spotipy
from spotipy.oauth2 import SpotifyOAuth

import os
from dotenv import load_dotenv

import csv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://127.0.0.1:8888",
        scope="user-library-read",
    )
)

results = sp.current_user_saved_tracks(limit=50)
tracks = results["items"]
total = results["total"]

while results["next"]:
    results = sp.next(results)
    tracks.extend(results["items"])
    print(f"Progress: {len(tracks)}/{total}")

with open("liked_songs.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["track", "artist", "album"])

    skipped = 0
    saved = 0

    for item in tracks:
        track = item["track"]
        
        if not track or not track.get("name") or not track.get("artists") or not track.get("album"):
            skipped += 1
            continue

        if not track.get("is_playable", True):
            skipped += 1
            continue

        album = track["album"]

        writer.writerow([
            track["name"],
            ', '.join([artist['name'] for artist in track['artists']]),
            album["name"],
            track["id"],
            album["id"],
            album["album_type"],
            album["total_tracks"]
        ])

        saved += 1

print(f"\nSaved: {saved}")

if skipped > 0:
    print(f"Skipped: {skipped}")
