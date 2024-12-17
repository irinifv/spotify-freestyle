import requests
import base64
import os
import time

class SpotifyAPIError(Exception):
    pass


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
        try:
            token = self.get_access_token()
            url = "https://api.spotify.com/v1/search"
            headers = {"Authorization": f"Bearer {token}"}
            params = {"q": artist_name, "type": "artist", "limit": 1}
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response_data = response.json()

            # Single set of debug logs
            print("API Request URL:", response.url)
            print("Response Status:", response.status_code)
            print("Response Data:", response_data)

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
                print("No artists found in API response for query:", artist_name)
                return None
                
            print("API Error Response:", response_data)
            raise SpotifyAPIError(f"Failed to search for artist: {response_data}")
                
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
