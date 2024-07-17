import itertools

from .data import load_from_zip
from .spotify import spotify_client


def main() -> None:
    data = load_from_zip('export.zip')
    ranked_tracks = data.votes.groupby('Spotify URI').sum().sort_values('Points Assigned')

    sp = spotify_client()
    user_id = sp.me()['id']

    playlist = sp.user_playlist_create(
        user_id,
        'Music League 3: Ranked',
        description='Submissions from Music League season 3 ranked by votes',
    )

    for chunk in itertools.batched(ranked_tracks.index.values[::-1], 50):
        sp.user_playlist_add_tracks(user_id, playlist['id'], chunk)
