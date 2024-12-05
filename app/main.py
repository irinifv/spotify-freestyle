import os
from dotenv import load_dotenv
from app.spotify_helpers import ensure_access_token, search_artist, get_related_artists, get_top_tracks
from app.visualization_helpers import plot_artist_popularity_interactive, plot_top_tracks_interactive

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

def main():
    # Ensure access token is valid
    ensure_access_token(CLIENT_ID, CLIENT_SECRET)

    # Get user input
    artist_name = input("Enter the name of an artist: ")
    artist = search_artist(artist_name)

    if artist:
        print(f"\nArtist: {artist['name']}")
        print(f"Popularity: {artist['popularity']}")
        print(f"Genres: {', '.join(artist['genres'])}")
        print(f"Followers: {artist['followers']['total']:,}")

        # Fetch related artists
        related_artists = get_related_artists(artist['id'])

        # Display popularity comparison
        plot_artist_popularity_interactive(artist['name'], artist['popularity'], related_artists)

        # Fetch and display top tracks
        top_tracks = get_top_tracks(artist['id'])
        plot_top_tracks_interactive(artist['name'], top_tracks)
    else:
        print("Artist not found!")

if __name__ == "__main__":
    main()