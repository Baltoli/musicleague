from music_league.hello import hello


def test_hello() -> None:
    assert hello('World') == 'Hello, World!'
