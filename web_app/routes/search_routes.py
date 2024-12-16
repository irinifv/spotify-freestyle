from flask import Flask, Blueprint, request, render_template, redirect, flash, url_for, current_app
import flask
from app.spotify_helpers import SpotifyAPI

# Initialize Flask Blueprint for routes
search_routes = Blueprint("search_routes", __name__)
spotify_api = SpotifyAPI()

# Home Route
@search_routes.route("/")
def home():
    """Render the homepage with a link to the search functionality."""
    return render_template("home.html", description="Welcome to the Spotify Artist Search App! Use the search page to find information about your favorite artists.")

# Search Route
@search_routes.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_query = request.form.get("query")

        if not search_query:
            flash("Please enter an artist name to search!", "danger")
            return redirect(url_for("search_routes.search"))
        
        spotify_api = current_app.config["SPOTIFY_API"]

        try:
            print(f"User query: {search_query}")
            artist_data = spotify_api.search_artist(search_query)

            # Debugging: Log the artist data
            print("Artist Data from SpotifyAPI:", artist_data)

            if not artist_data:
                flash("No results found for the artist!", "warning")
                return redirect(url_for("search_routes.search"))

            return render_template("search_results.html", artist=artist_data)

        except Exception as e:
            print(f"Error occurred during Spotify API call for query '{search_query}': {e}")
            flash("An error occurred while processing your request. Please try again.", "danger")
            return redirect(url_for("search_routes.search"))

    return render_template("search.html")

