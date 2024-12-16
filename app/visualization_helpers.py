#visualization_helpers.py
# contains functions to create interactive visualizations using Plotly
# these functions will be used in the main.py file to generate interactive visualizations

import plotly.express as px

# Plot artist popularity and related artists
def plot_artist_popularity_interactive(artist_name, artist_popularity, related_artists):
    print(f"Debug - Inputs: {artist_name}, {artist_popularity}, {related_artists[:2]}...")
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


def plot_album_timeline_interactive(albums):
    # Enhanced debug info
    print(f"Debug - Number of albums: {len(albums)}")
    if not albums:
        print("Warning: No albums provided")
        return px.scatter(title="No Album Data Available")
        
    print("Debug - Album details:")
    for album in albums[:2]:  # Show first 2 albums
        print(f"  - {album.get('name', 'No name')}: {album.get('release_date', 'No date')}")

    sorted_albums = sorted(albums, key=lambda x: x['release_date'])
    album_names = [album['name'] for album in sorted_albums]
    release_dates = [album['release_date'] for album in sorted_albums]
    
    fig = px.scatter(
        x=release_dates,
        y=[1] * len(release_dates),
        text=album_names,
        title="Album Release Timeline",
        labels={"x": "Release Date", "y": ""},
        hover_data={
            'Album': album_names,
            'Release Date': release_dates
        }
    )
    
    fig.update_traces(
        marker=dict(size=12, color='blue'),
        textposition='top center'
    )
    fig.update_layout(
        showlegend=False,
        yaxis_visible=False,
        yaxis_showticklabels=False,
        xaxis_title="Release Date",
        height=400,
        margin=dict(t=50, b=50)
    )
    
    return fig



# def plot_album_timeline_interactive(albums):
#     print(f"Debug - Number of albums: {len(albums)}")
#     print(f"Debug - First album: {albums[0] if albums else 'No albums'}")
#     sorted_albums = sorted(albums, key=lambda x: x['release_date'])
#     album_names = [album['name'] for album in sorted_albums]
#     release_dates = [album['release_date'] for album in sorted_albums]
    
#     fig = px.scatter(
#         x=release_dates,
#         y=[1] * len(release_dates),  # All points on same y-level
#         text=album_names,
#         title="Album Release Timeline",
#         labels={"x": "Release Date", "y": ""},
#     )
    
#     # Customize layout
#     fig.update_traces(marker=dict(size=10))
#     fig.update_layout(
#         showlegend=False,
#         yaxis_visible=False,
#         yaxis_showticklabels=False
#     )
    
#     return fig




# # Plot album release timeline
# def plot_album_timeline_interactive(albums):
#     sorted_albums = sorted(albums, key=lambda x: x['release_date'])
#     album_names = [album['name'] for album in sorted_albums]
#     release_dates = [album['release_date'] for album in sorted_albums]
#     fig = px.scatter(
#         x=release_dates,
#         y=album_names,
#         title="Album Release Timeline",
#         labels={"x": "Release Date", "y": "Albums"}
    
#     )
#     return fig

