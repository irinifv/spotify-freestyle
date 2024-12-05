import pytest
from app.visualization_helpers import (
    plot_artist_popularity_interactive, plot_album_timeline_interactive
)
from unittest.mock import patch

def test_plot_artist_popularity_interactive():
    # Test does not verify rendering; ensures no exceptions raised
    try:
        plot_artist_popularity_interactive(
            "Mock Artist", 80, [{"name": "Related Artist", "popularity": 70}]
        )
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")

def test_plot_album_timeline_interactive():
    albums = [
        {"name": "Album 1", "release_date": "2021-01-01"},
        {"name": "Album 2", "release_date": "2022-01-01"}
    ]
    try:
        plot_album_timeline_interactive(albums)
    except Exception as e:
        pytest.fail(f"Unexpected error: {e}")