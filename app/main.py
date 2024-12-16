#main.py
# contains the main code for the Flask web application
# this file will be used to run the Flask web application
# it imports the SpotifyAPI class from spotify_helpers.py and the visualization functions from visualization_helpers.py
# it also defines the routes for the web application and renders the appropriate templates

from flask import Flask, request, jsonify, render_template
from app.spotify_helpers import SpotifyAPI
from app.visualization_helpers import plot_artist_popularity_interactive, plot_album_timeline_interactive

# Initialize Flask app
app = Flask(__name__)
spotify_api = SpotifyAPI()

# Define routes

# Home route
@app.route("/")
def home():
    return render_template("home.html")

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