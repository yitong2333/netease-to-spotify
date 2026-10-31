import pytest

from src import netease


def test_daily_recommendations_use_api_service_and_normalize_response(monkeypatch, capsys):
    request = {}
    songs = [
        {
            "name": f"Test Song {index:02d}",
            "ar": [{"name": "Test Artist"}],
            "al": {"name": "Test Album"},
            "dt": 180000,
        }
        for index in range(1, 33)
    ]

    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {"code": 200, "data": {"dailySongs": songs}}

    def fake_get(url, **kwargs):
        request["url"] = url
        request.update(kwargs)
        return Response()

    monkeypatch.setattr(netease.requests, "get", fake_get)

    result = netease.get_daily_recommendations(
        "MUSIC_U=session; __csrf=csrf-token",
        api_base_url="https://music-api.example.com/",
        verbose=False,
    )

    assert request["url"] == "https://music-api.example.com/recommend/songs"
    assert request["params"] == {}
    assert request["headers"]["Cookie"] == "MUSIC_U=session; __csrf=csrf-token"
    assert len(result) == 32
    assert result[0] == {
        "name": "Test Song 01",
        "artists": ["Test Artist"],
        "album": "Test Album",
        "duration_ms": 180000,
    }
    output = capsys.readouterr().out
    assert "Found 32 NetEase daily recommendations." in output
    assert "Test Song 01" not in output


def test_private_radar_tracks_fetch_playlist_and_handles_string_artist(monkeypatch):
    request = {}

    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "code": 200,
                "songs": [
                    {
                        "name": "Radar Song",
                        "artists": "Artist One / Artist Two",
                        "album": {"name": "Radar Album"},
                        "duration_ms": 190000,
                    }
                ],
            }

    def fake_get(url, **kwargs):
        request["url"] = url
        request.update(kwargs)
        return Response()

    monkeypatch.setattr(netease.requests, "get", fake_get)

    result = netease.get_private_radar_tracks(
        "MUSIC_U=session",
        api_base_url="https://music-api.example.com",
        verbose=False,
    )

    assert request["url"] == "https://music-api.example.com/playlist/track/all"
    assert request["params"] == {
        "id": "3136952023",
        "limit": 1000,
        "offset": 0,
    }
    assert request["headers"]["Cookie"] == "MUSIC_U=session"
    assert result == [
        {
            "name": "Radar Song",
            "artists": ["Artist One", "Artist Two"],
            "album": "Radar Album",
            "duration_ms": 190000,
        }
    ]


def test_api_base_url_must_be_configured(monkeypatch):
    monkeypatch.delenv("NETEASE_API_BASE_URL", raising=False)

    with pytest.raises(RuntimeError, match="NETEASE_API_BASE_URL"):
        netease._api_url("recommend/songs")


def test_api_base_url_requires_http_scheme():
    with pytest.raises(ValueError, match="http:// or https://"):
        netease._api_url("recommend/songs", "music-api.example.com")
