import plotly.express as px

def plot_artist_popularity_interactive(artist_name, artist_popularity, related_artists):
    """
    Create an interactive bar chart comparing artist popularity.
    """
    names = [artist_name] + [artist['name'] for artist in related_artists[:5]]
    popularities = [artist_popularity] + [artist['popularity'] for artist in related_artists[:5]]

    fig = px.bar(
        x=names,
        y=popularities,
        title=f"Popularity Comparison: {artist_name} and Related Artists",
        labels={"x": "Artists", "y": "Popularity"},
        text=popularities,
        color=popularities,
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig.update_traces(textposition='outside')
    fig.show()

def plot_top_tracks_interactive(artist_name, top_tracks):
    """
    Create an interactive bar chart showing an artist's top tracks.
    """
    track_names = [track['name'] for track in top_tracks]
    popularities = [track['popularity'] for track in top_tracks]

    fig = px.bar(
        x=track_names,
        y=popularities,
        title=f"Top Tracks of {artist_name}",
        labels={"x": "Tracks", "y": "Popularity"},
        text=popularities,
        color=popularities,
        color_continuous_scale=px.colors.sequential.Viridis
    )
    fig.update_traces(textposition='outside')
    fig.show()
