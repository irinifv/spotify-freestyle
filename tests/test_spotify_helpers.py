import pytest
from unittest.mock import patch
from app.spotify_helpers import (
    get_access_token,
    search_artist,
    get_top_tracks,
    get_related_artists,
    get_artist_albums,
    get_artist_collaborations,
)

@pytest.fixture
def mock_access_token():
    """Fixture to provide a mock access token."""
    return "mock_access_token"

def test_get_access_token():
    """Test for fetching an access token."""
    with patch("app.spotify_helpers.requests.post") as mock_post:
        mock_response = mock_post.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "mock_token"}

        access_token = get_access_token("mock_client_id", "mock_client_secret")
        assert access_token == "mock_token"

def test_search_artist(mock_access_token):
    """Test searching for an artist."""
    with patch("app.spotify_helpers.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "artists": {
                "items": [{"id": "123", "name": "Mock Artist", "popularity": 80}]
            }
        }
        artist = search_artist("Mock Artist")
        assert artist is not None
        assert artist["id"] == "123"
        assert artist["name"] == "Mock Artist"
        assert artist["popularity"] == 80

def test_get_top_tracks(mock_access_token):
    """Test fetching top tracks for an artist."""
    with patch("app.spotify_helpers.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tracks": [
                {"name": "Track 1", "album": {"name": "Album 1"}},
                {"name": "Track 2", "album": {"name": "Album 2"}}
            ]
        }
        top_tracks = get_top_tracks(mock_access_token, "artist_id")
        assert len(top_tracks) == 2
        assert top_tracks[0]["name"] == "Track 1"
        assert top_tracks[0]["album"]["name"] == "Album 1"

def test_get_related_artists(mock_access_token):
    """Test fetching related artists."""
    with patch("app.spotify_helpers.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "artists": [{"name": "Related Artist", "popularity": 60}]
        }
        related_artists = get_related_artists(mock_access_token, "artist_id")
        assert len(related_artists) == 1
        assert related_artists[0]["name"] == "Related Artist"

def test_get_artist_albums(mock_access_token):
    """Test fetching an artist's albums."""
    with patch("app.spotify_helpers.requests.get") as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "items": [{"name": "Album 1", "release_date": "2022-01-01"}]
        }
        albums = get_artist_albums(mock_access_token, "artist_id")
        assert len(albums) == 1
        assert albums[0]["name"] == "Album 1"
        assert albums[0]["release_date"] == "2022-01-01"

def test_get_artist_collaborations(mock_access_token):
    """Test fetching an artist's collaborations."""
    with patch("app.spotify_helpers.get_top_tracks") as mock_get_top_tracks:
        mock_get_top_tracks.return_value = [
            {"artists": [{"id": "123", "name": "Artist 1"}, {"id": "artist_id", "name": "Main Artist"}]},
            {"artists": [{"id": "456", "name": "Artist 2"}, {"id": "artist_id", "name": "Main Artist"}]}
        ]
        collaborations = get_artist_collaborations(mock_access_token, "artist_id")
        assert "Artist 1" in collaborations
        assert "Artist 2" in collaborations
