from flask import Blueprint, request, render_template, redirect, flash, url_for, current_app
from app.spotify_helpers import SpotifyAPI

# Initialize Flask Blueprint for routes
search_routes = Blueprint("search_routes", __name__)

@search_routes.route("/")
def home():
    """Render the homepage with a link to the search functionality."""
    return render_template("home.html", description="Welcome to the Spotify Artist Search App!")

@search_routes.route("/search/form")
def search_form():
    """Display the search form page"""
    return render_template("search.html")

@search_routes.route("/search/results", methods=["GET", "POST"])
def search_results():
    """Handle the search results page with both GET and POST methods"""
    
    if request.method == "POST":
        # For data sent via POST request, form inputs are in request.form
        search_query = request.form.get("query")
    else:
        # For data sent via GET request, url params are in request.args
        search_query = request.args.get("query")

    if not search_query:
        flash("Please enter an artist name to search!", "danger")
        return redirect(url_for("search_routes.search_form"))
    
    spotify_api = current_app.config["SPOTIFY_API"]

    try:
        print(f"User query: {search_query}")
        artist_data = spotify_api.search_artist(search_query)

        # Debugging: Log the artist data
        print("Artist Data from SpotifyAPI:", artist_data)

        if not artist_data:
            flash("No results found for the artist!", "warning")
            return redirect(url_for("search_routes.search_form"))

        return render_template("search_results.html", artist=artist_data)

    except Exception as e:
        print(f"Error occurred during Spotify API call for query '{search_query}': {e}")
        flash("An error occurred while processing your request. Please try again.", "danger")
        return redirect(url_for("search_routes.search_form"))

# API Routes
@search_routes.route("/api/search.json")
def search_api():
    """JSON API endpoint for artist search"""
    search_query = request.args.get("query")
    
    if not search_query:
        return {"message": "Please provide a search query"}, 400
    
    try:
        spotify_api = current_app.config["SPOTIFY_API"]
        artist_data = spotify_api.search_artist(search_query)
        
        if not artist_data:
            return {"message": "No results found"}, 404
            
        return {"artist": artist_data}
        
    except Exception as e:
        print(f"API Error: {str(e)}")
        return {"message": "An error occurred while processing your request"}, 500
