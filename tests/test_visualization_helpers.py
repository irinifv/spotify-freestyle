from app.visualization_helpers import plot_artist_popularity_interactive, plot_top_tracks_interactive

def test_plot_artist_popularity_interactive():
    # Test if the function runs without errors
    artist_name = "Test Artist"
    artist_popularity = 80
    related_artists = [
        {"name": "Related Artist 1", "popularity": 70},
        {"name": "Related Artist 2", "popularity": 60},
    ]
    plot_artist_popularity_interactive(artist_name, artist_popularity, related_artists)
    # No assertions as we are testing visualization rendering

def test_plot_top_tracks_interactive():
    # Test if the function runs without errors
    artist_name = "Test Artist"
    top_tracks = [
        {"name": "Track 1", "popularity": 90},
        {"name": "Track 2", "popularity": 85},
    ]
    plot_top_tracks_interactive(artist_name, top_tracks)
    # No assertions as we are testing visualization rendering