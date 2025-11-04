import spotipy
from spotipy.oauth2 import SpotifyOAuth

import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = client_id,
                                               client_secret = client_secret,
                                               redirect_uri = "http://127.0.0.1:8888",
                                               scope = "user-library-read"))

artist_uri = "spotify:artist:0Y5tJX1MQlPlqiwlOH1tJY"

results = sp.artist_albums(artist_uri, album_type="album")
albums = results["items"]

while results["next"]:
    results = sp.next(results)
    albums.extend(results["items"])

for album in albums:
    print(album["name"])
