import requests
import base64
import time
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

class SpotifyAPI:
    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.access_token = None
        self.token_expiry_time = None

    def get_access_token(self):
        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        }
        data = {"grant_type": "client_credentials"}
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            self.token_expiry_time = time.time() + 3600  # Token valid for 1 hour
            self.access_token = response.json()["access_token"]
        else:
            raise Exception("Error fetching access token:", response.json())

    def ensure_access_token(self):
        if not self.access_token or time.time() >= self.token_expiry_time:
            self.get_access_token()

    def search_artist(self, artist_name):
        self.ensure_access_token()
        url = "https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {"q": artist_name, "type": "artist", "limit": 1}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            artists = response.json().get("artists", {}).get("items", [])
            return artists[0] if artists else None
        else:
            raise Exception("Error searching for artist:", response.json())

    def get_top_tracks(self, artist_id):
        self.ensure_access_token()
        url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {"market": "US"}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("tracks", [])
        else:
            raise Exception("Error fetching top tracks:", response.json())

    def get_related_artists(self, artist_id):
        self.ensure_access_token()
        url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("artists", [])
        else:
            raise Exception("Error fetching related artists:", response.json())

    def get_artist_albums(self, artist_id):
        self.ensure_access_token()
        url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {"include_groups": "album", "limit": 50}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json().get("items", [])
        else:
            raise Exception("Error fetching albums:", response.json())
