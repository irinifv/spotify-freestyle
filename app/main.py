#main.py
# contains the main code for the Flask web application
# this file will be used to run the Flask web application
# it imports the SpotifyAPI class from spotify_helpers.py and the visualization functions from visualization_helpers.py
# it also defines the routes for the web application and renders the appropriate templates

import sys
import os
from flask import Flask, request, redirect, jsonify, render_template, url_for, session

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.spotify_helpers import SpotifyAPI
from app.visualization_helpers import plot_artist_popularity_interactive, plot_album_timeline_interactive

# Initialize Flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.random(64)

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = "http://localhost:5000/callback"
scope = "playlist-read-private"

cache_handler = FlaskSessionCacheHandler(session=app)

sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)

sp = Spotify(auth_manager=sp_oauth)

spotify_api = SpotifyAPI()

# Define routes

# Home route
@app.route("/")
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return render_template("home.html")
    return redirect(url_for("get_playlists"))


# Search route
@app.route("/search", methods=["POST"])
def search_artist():
    artist_name = request.form["artist_name"]
    artist = spotify_api.search_artist(artist_name)

    if not artist:
        return render_template("spotify_data.html", artist=None)

    related_artists = spotify_api.get_related_artists(artist["id"])
    fig = plot_artist_popularity_interactive(artist["name"], artist["popularity"], related_artists)

    return render_template(
        "spotify_data.html",
        artist=artist,
        related_artists=related_artists,
        fig=fig.to_html()
    )

if __name__ == "__main__":
    app.run(debug=True)