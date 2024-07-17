import os

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth


def _client_id() -> str:
    return os.environ['SPOTIFY_CLIENT_ID']


def _client_secret() -> str:
    return os.environ['SPOTIFY_CLIENT_SECRET']


def _redirect_uri() -> str:
    return os.environ['SPOTIFY_REDIRECT_URI']


def spotify_client() -> Spotify:
    return Spotify(
        auth_manager=SpotifyOAuth(
            client_id=_client_id(),
            client_secret=_client_secret(),
            redirect_uri=_redirect_uri(),
            scope='user-library-read,playlist-modify-public',
        )
    )
