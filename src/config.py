import os
from dataclasses import dataclass

from .match_levels import DEFAULT_MATCH_LEVEL, normalize_match_level


@dataclass(frozen=True)
class Settings:
    spotify_client_id: str
    spotify_client_secret: str
    spotify_refresh_token: str
    spotify_playlist_id: str
    netease_cookie: str
    spotify_radar_playlist_id: str | None = None
    match_level: str = DEFAULT_MATCH_LEVEL


REQUIRED_ENV_VARS = (
    "SPOTIFY_CLIENT_ID",
    "SPOTIFY_CLIENT_SECRET",
    "SPOTIFY_REFRESH_TOKEN",
    "SPOTIFY_PLAYLIST_ID",
    "NETEASE_COOKIE",
)


def load_settings() -> Settings:
    for name in REQUIRED_ENV_VARS:
        if not os.getenv(name):
            raise RuntimeError(f"Missing required environment variable: {name}")

    match_level = normalize_match_level(os.getenv("MATCH_LEVEL"))

    return Settings(
        spotify_client_id=os.environ["SPOTIFY_CLIENT_ID"],
        spotify_client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
        spotify_refresh_token=os.environ["SPOTIFY_REFRESH_TOKEN"],
        spotify_playlist_id=os.environ["SPOTIFY_PLAYLIST_ID"],
        netease_cookie=os.environ["NETEASE_COOKIE"],
        spotify_radar_playlist_id=os.getenv("SPOTIFY_RADAR_PLAYLIST_ID") or None,
        match_level=match_level,
    )
