import pytest
from app.spotify_helpers import get_access_token, search_artist, get_related_artists, get_top_tracks

@pytest.fixture
def mock_credentials():
    return {"client_id": "mock_client_id", "client_secret": "mock_client_secret"}

def test_get_access_token(monkeypatch, mock_credentials):
    def mock_post(*args, **kwargs):
        class MockResponse:
            def json(self):
                return {"access_token": "mock_token"}
            @property
            def status_code(self):
                return 200
        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)
    token = get_access_token(mock_credentials["client_id"], mock_credentials["client_secret"])
    assert token == "mock_token"

def test_search_artist(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def json(self):
                return {"artists": {"items": [{"name": "Mock Artist", "id": "mock_id"}]}}
            @property
            def status_code(self):
                return 200
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    artist = search_artist("Mock Artist")
    assert artist["name"] == "Mock Artist"

# Add more tests

def test_get_access_token_invalid_credentials(monkeypatch, mock_credentials):
    def mock_post(*args, **kwargs):
        class MockResponse:
            def json(self):
                return {"error": "invalid_client"}
            @property
            def status_code(self):
                return 401
        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)
    token = get_access_token(mock_credentials["client_id"], mock_credentials["client_secret"])
    assert token is None

def test_get_access_token_missing_credentials():
    token = get_access_token(None, None)
    assert token is None

def test_search_artist_not_found(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def json(self):
                return {"artists": {"items": []}}
            @property
            def status_code(self):
                return 200
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    artist = search_artist("Nonexistent Artist")
    assert artist is None

def test_search_artist_invalid_query(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def json(self):
                return {"error": {"message": "Invalid search query"}}
            @property
            def status_code(self):
                return 400
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    artist = search_artist("")
    assert artist is None

def test_get_top_tracks_no_tracks(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def json(self):
                return {"tracks": []}
            @property
            def status_code(self):
                return 200
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    tracks = get_top_tracks("mock_token", "mock_artist_id")
    assert tracks == []

def test_get_top_tracks_invalid_artist_id(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def json(self):
                return {"error": {"message": "Artist not found"}}
            @property
            def status_code(self):
                return 404
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    tracks = get_top_tracks("mock_token", "invalid_artist_id")
    assert tracks == []

def test_get_related_artists_no_results(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def json(self):
                return {"artists": []}
            @property
            def status_code(self):
                return 200
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    related_artists = get_related_artists("mock_token", "mock_artist_id")
    assert related_artists == []

def test_get_related_artists_invalid_token(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def json(self):
                return {"error": {"message": "Invalid access token"}}
            @property
            def status_code(self):
                return 401
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    related_artists = get_related_artists("invalid_token", "mock_artist_id")
    assert related_artists == []

def test_get_artist_albums_no_albums(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def json(self):
                return {"items": []}
            @property
            def status_code(self):
                return 200
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    albums = get_artist_albums("mock_token", "mock_artist_id")
    assert albums == []

def test_get_artist_albums_pagination(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def json(self):
                return {
                    "items": [{"name": "Album 1"}, {"name": "Album 2"}],
                    "next": None,  # Simulate end of pagination
                }
            @property
            def status_code(self):
                return 200
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    albums = get_artist_albums("mock_token", "mock_artist_id")
    assert len(albums) == 2
    assert albums[0]["name"] == "Album 1"