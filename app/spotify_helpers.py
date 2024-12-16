import requests
import base64
import os
import time

class SpotifyAPI:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.access_token = None
        self.token_expiry_time = None

    def get_access_token(self):
        """Retrieve a new access token from Spotify."""
        if self.access_token and self.token_expiry_time > time.time():
            return self.access_token

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        }
        data = {"grant_type": "client_credentials"}

        response = requests.post(url, headers=headers, data=data)
        response_data = response.json()

        # Debugging Logs
        print("Access Token Response:", response_data)

        if response.status_code == 200:
            self.access_token = response_data.get("access_token")
            self.token_expiry_time = time.time() + response_data.get("expires_in", 3600)
            return self.access_token
        else:
            print("Failed to retrieve access token:", response_data)
            raise Exception(f"Failed to retrieve access token: {response_data}")

    def search_artist(self, artist_name):
        """Search for an artist by name."""
        token = self.get_access_token()
        url = "https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {token}"}
        params = {"q": artist_name, "type": "artist", "limit": 1}

        response = requests.get(url, headers=headers, params=params)

        # Debugging Logs
        print("API Request URL:", response.url)
        print("Request Headers:", headers)
        print("Response Status Code:", response.status_code)
        print("Response JSON:", response.json())

        response_data = response.json()

        # Debugging Logs
        print("API Request URL:", response.url)
        print("API Response:", response_data)

        if response.status_code == 200:
            artists = response_data.get("artists", {}).get("items", [])
            if artists:
                artist = artists[0]
                return {
                    "name": artist.get("name"),
                    "genres": artist.get("genres", []),
                    "popularity": artist.get("popularity"),
                    "external_urls": artist.get("external_urls", {}).get("spotify", ""),
                }
            else:
                print("No artists found in API response for query:", artist_name)
                return None
        else:
            print("API Error Response:", response_data)
            raise Exception(f"Failed to search for artist: {response_data}")

        return None
