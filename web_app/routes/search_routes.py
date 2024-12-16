from flask import Blueprint, request, render_template, redirect, flash, url_for

from app.spotify_helpers import SpotifyAPI

search_routes = Blueprint("search_routes", __name__)

spotify_api = SpotifyAPI()

#search for an artist by name
@search_routes.route("/search", methods=["GET", "POST"])
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
            return redirect(url_for("search_routes.search"))

        try:
            artist = spotify_api.search_artist(search_query)
            if not artist:
                flash("Artist not found!", "warning")
                return redirect(url_for("search_routes.search"))

            top_tracks = spotify_api.get_top_tracks(artist["id"])
            related_artists = spotify_api.get_related_artists(artist["id"])

            return render_template(
                "search_results.html",
                artist=artist,
                top_tracks=top_tracks,
                related_artists=related_artists
            )
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
            return redirect(url_for("search_routes.search"))

    return render_template("search.html")


#artist route
@search_routes.route("/artists/<artist_id>", methods=["POST", "GET"])
def artist(artist_id):
    """
    Handle the artist page.
    """
    print("ARTIST route accessed.")

    artist = spotify_api.search_artist(artist_id)
    if not artist:
        flash("Artist not found!", "warning")
        return redirect(url_for("search_routes.search"))

    related_artists = spotify_api.get_related_artists(artist_id)
    return render_template("artist.html", artist=artist, related_artists=related_artists)


@search_routes.route("/albums/<artist_id>")
def albums(artist_id):
    """
    Handle the albums page.
    """
    print("ALBUMS route accessed.")

    artist = spotify_api.search_artist_by_id(artist_id)
    if not artist:
        flash("Artist not found!", "warning")
        return redirect(url_for("search_routes.search"))

    albums = spotify_api.get_artist_albums(artist_id)
    return render_template("albums.html", artist=artist, albums=albums)