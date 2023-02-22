import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = '01d7a7c492a743a08d0bbce6dba0334a'
CLIENT_SECRET = '8ce6d320462b43ad83e2683c76237203'
REDIRECT_URI = "http://localhost:8888/callback/"
USERNAME = 'bobobubs'
PLAYLIST_NAME = 'Test Playlist'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=['playlist-modify-public']))
playlist = sp.user_playlist_create(
    user=USERNAME, name=PLAYLIST_NAME, public=True)
