import requests
import time
import base64

# Global variables for token and expiry
access_token = None
token_expiry_time = None

def get_access_token(client_id, client_secret):
    """
    Fetch a new access token from the Spotify API.
    """
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    }
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        global token_expiry_time
        token_expiry_time = time.time() + 3600  # Token valid for 1 hour
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to get access token: {response.json()}")

def ensure_access_token(client_id, client_secret):
    """
    Ensure the global access token is valid.
    """
    global access_token, token_expiry_time
    if not access_token or time.time() >= token_expiry_time:
        access_token = get_access_token(client_id, client_secret)

def search_artist(artist_name):
    """
    Search for an artist by name.
    """
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": artist_name, "type": "artist", "limit": 1}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        artists = response.json().get("artists", {}).get("items", [])
        return artists[0] if artists else None
    else:
        raise Exception(f"Failed to search artist: {response.json()}")

def get_related_artists(artist_id):
    """
    Fetch related artists for a given artist ID.
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/related-artists"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("artists", [])
    else:
        raise Exception(f"Failed to fetch related artists: {response.json()}")

def get_top_tracks(artist_id, market="US"):
    """
    Fetch top tracks for a given artist ID.
    """
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"market": market}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("tracks", [])
    else:
        raise Exception(f"Failed to fetch top tracks: {response.json()}")