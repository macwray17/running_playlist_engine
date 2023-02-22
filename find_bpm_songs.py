import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class Playlist_Engine:
    def __init__(self, client_id, client_secret, oauth_token):
        # Your Spotify API credentials
        self.CLIENT_ID = client_id
        self.CLIENT_SECRET = client_secret
        self.OAUTH_TOKEN = oauth_token
        self.REDIRECT_URI = "http://localhost:8888/callback/"
        self.USERNAME = 'bobobubs'

        # define member variable
        self.seed_artists = ""
        self.seed_tracks = ""
        self.seed_genres = ""
        self.taget_tempo = ""
        self.playlist_name = "Engine Created"
        self.playlist_id = ''
        self.playlist_tracks = []

        # Request an access token
        self.auth_response = requests.post("https://accounts.spotify.com/api/token",
                                           data={
                                               "grant_type": "client_credentials",
                                               "client_id": self.CLIENT_ID,
                                               "client_secret": self.CLIENT_SECRET,
                                           }
                                           )
        self.access_token = self.auth_response.json()["access_token"]

        self.headers = {
            "Authorization": f"Bearer {oauth_token}"
        }

        # create a spotipy object
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.CLIENT_ID,
                                                            client_secret=self.CLIENT_SECRET,
                                                            redirect_uri=self.REDIRECT_URI,
                                                            scope=['playlist-modify-public']))

    def reccomend_bpm_songs(self, target_tempo, limit):
        # Set the number of recommended tracks you want to retrieve
        url = f"https://api.spotify.com/v1/recommendations?"
        url += f"seed_artists={self.seed_artists}&limit={limit}&seed_genres={self.seed_genres}&seed_tracks={self.seed_tracks}&target_tempo={target_tempo}"
        # Search for tracks
        response = requests.get(url, headers=self.headers)
        print(response)
        print("RESPONSE STATUS CODE", response.status_code)

        if response.status_code == 200:
            recommendations = response.json().get("tracks")
            for track in recommendations:
                print("Track Name:", track.get("name"))
                print("Track ID:", track.get("id"))
                print("Artist Name:", track["artists"][0].get("name"))
                print("Artist ID:", track["artists"][0].get('id'))
                print("Preview URL:", track.get("preview_url"))
                print("-" * 20)
                print(track["artists"][0].get('id'))

                self.playlist_tracks.append(track['uri'])
        else:
            print("Could not retrieve recommendations")

    def make_playlist(self):
        self.playlist = self.sp.user_playlist_create(
            user=self.USERNAME, name=self.playlist_name, public=True)
        self.playlist_id = self.playlist['id']
        self.sp.user_playlist_add_tracks(
            user=self.USERNAME, playlist_id=self.playlist_id, tracks=self.playlist_tracks)

    def addSeedArtist(self, artist_name):
        results = self.sp.search(q=artist_name, type="artist")
        # Get the first result from the search results
        artist = results["artists"]["items"][0]
        # Get the artist ID
        artist_id = artist["id"]
        if self.seed_artists == "":
            self.seed_artists += artist_id
        else:
            self.seed_artists += "," + artist_id

    def addSeedTrack(self, track_name, artist_name):
        q = f"artist:{artist_name} track:{track_name}"
        results = self.sp.search(q=q, type="track", limit=1)
        # get the track_id
        track_id = results["tracks"]["items"][0]["id"]
        if self.seed_tracks == "":
            self.seed_tracks += track_id
        else:
            self.seed_tracks += "," + track_id

    def get_artist_id(self, artist_name):
        results = self.sp.search(q=artist_name, type="artist")
        # Get the first result from the search results
        artist = results["artists"]["items"][0]
        # Get the artist ID
        artist_id = artist["id"]
        print("The artist ID of {} is {}".format(artist_name, artist_id))
        return artist_id

    def get_track_id(self, song_name, artist_name):
        q = f"artist:{artist_name} track:{song_name}"
        results = self.sp.search(q=q, type="track", limit=1)
        # get the track_id
        track_id = results["tracks"]["items"][0]["id"]
        print("The track ID of {} by {} is {}".format(
            song_name, artist_name, id))
        return track_id
