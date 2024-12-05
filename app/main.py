from flask import Flask, request, jsonify, render_template
from app.spotify_helpers import SpotifyAPI
from app.visualization_helpers import plot_artist_popularity_interactive, plot_album_timeline_interactive

app = Flask(__name__)
spotify_api = SpotifyAPI()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search_artist():
    artist_name = request.form["artist_name"]
    artist = spotify_api.search_artist(artist_name)
    if not artist:
        return jsonify({"error": "Artist not found"}), 404
    related_artists = spotify_api.get_related_artists(artist["id"])
    fig = plot_artist_popularity_interactive(artist["name"], artist["popularity"], related_artists)
    return fig.to_html()

if __name__ == "__main__":
    app.run(debug=True)