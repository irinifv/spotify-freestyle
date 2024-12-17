#visualization_helpers.py
# contains functions to create interactive visualizations using Plotly
# these functions will be used in the main.py file to generate interactive visualizations

import plotly.express as px

# Plot artist popularity and related artists
def plot_artist_popularity_interactive(artist_name, artist_popularity, related_artists):
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
    fig.update_layout(xaxis_tickangle=-45)
    return fig

# Plot album release timeline
def plot_album_timeline_interactive(albums):
    sorted_albums = sorted(albums, key=lambda x: x['release_date'])
    album_names = [album['name'] for album in sorted_albums]
    release_dates = [album['release_date'] for album in sorted_albums]
    fig = px.scatter(
        x=release_dates,
        y=album_names,
        title="Album Release Timeline",
        labels={"x": "Release Date", "y": "Albums"}
    )
    return fig

