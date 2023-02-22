import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = 'put client id here'
CLIENT_SECRET = 'put client secret here.'
REDIRECT_URI = "http://localhost:8888/callback/"
USERNAME = 'bobobubs'
PLAYLIST_NAME = 'Test Playlist'

artist_name = "INTERWORLD"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=['playlist-modify-public']))


def get_artist_id(artist_name):
    results = sp.search(q=artist_name, type="artist")

    # Get the first result from the search results
    artist = results["artists"]["items"][0]

    # Get the artist ID
    artist_id = artist["id"]

    print("The artist ID of {} is {}".format(artist_name, artist_id))
    return artist_id


def get_track_id(song_name, artist_name):
    q = f"artist:{artist_name} track:{song_name}"
    results = sp.search(q=q, type="track", limit=1)
    id = results["tracks"]["items"][0]["id"]
    print("The track ID of {} by {} is {}".format(
        song_name, artist_name, id))
    return id


def addSeedArtist(seed_artists, artist_id):
    if seed_artists == "":
        seed_artists += artist_id
    else:
        seed_artists += "," + artist_id
    return seed_artists


def addSeedTrack(seed_tracks, track_id):
    if seed_tracks == "":
        seed_tracks += track_id
    else:
        seed_tracks += "," + track_id
    return seed_tracks
