from flask import Blueprint, request, render_template, redirect, flash, url_for

from app.spotify_helpers import SpotifyAPI

source_routes = Blueprint("source_routes", __name__)

spotify_api = SpotifyAPI()

@source_routes.route("/search", methods=["GET", "POST"])
def search():
    """
    Handle search functionality.
    If POST: process search form input.
    If GET: render search page.
    """
    print("SEARCH route accessed.")

    if request.method == "POST":
        # Extract search query from form
        search_query = request.form.get("query")
        print("SEARCH QUERY:", search_query)

        if not search_query:
            # Redirect back to the search page if query is missing
            flash("Search query cannot be empty!", "danger")
            return redirect(url_for("source_routes.search"))

        artist = spotify_api.search_artist(search_query)
        if not artist:
            flash("Artist not found!", "warning")
            return redirect(url_for("source_routes.search"))

        top_tracks = spotify_api.get_top_tracks(artist["id"])
        # related_artists = spotify_api.get_related_artists(artist["id"])

        return render_template(
            "search_results.html",
            artist=artist,
            top_tracks=top_tracks,
            # related_artists=related_artists
        )

    return render_template("search.html")

@source_routes.route("/albums/<artist_id>")
def albums(artist_id):
    """
    Handle the albums page.
    """
    print("ALBUMS route accessed.")

    artist = spotify_api.search_artist_by_id(artist_id)
    if not artist:
        flash("Artist not found!", "warning")
        return redirect(url_for("source_routes.search"))

    albums = spotify_api.get_artist_albums(artist_id)
    return render_template("albums.html", artist=artist, albums=albums)