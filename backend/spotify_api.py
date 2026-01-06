from pydantic import BaseModel                     # Helps with type check and type conversion
import os                                          # Get environmental variables
from dotenv import load_dotenv                     # Load the keys in the env file
from fastapi import Body, Header                   # Helps format data sent to Spotify API
import requests                                    # HTTP client used to make API requests(For Spotify)
from urllib.parse import urlencode                 # Helps format URLs(Spotify reqs specifc URL formats)


""" Spotify API Set up """
load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URL = os.getenv("SPOTIFY_REDIRECT_URL")


""" Spotify Pydantic Obj Set Up """
class SpotifyToYoutube(BaseModel):
    name: str
    username: str
    password: str
    spotify_playlist_link: str

class SpotifySongURI(BaseModel):
    track_uris: list[str]

class YouTubeToSpotifyTransfer(BaseModel):
    youtube_playlist_id: str
    spotify_playlist_name: str

SPOTIFY_SCOPE = (
    "playlist-modify-private "
    "playlist-modify-public "
    "playlist-read-private "
    "playlist-read-collaborative"
)


""" Get Spotify API key """
load_dotenv()
API_KEY = os.getenv("SPOTIFY_API_KEY")


""" Spotify API helper functions """
def login_spotify_helper():
    parameters = {
        "response_type": "code",
        "client_id": SPOTIFY_CLIENT_ID,
        "scope": SPOTIFY_SCOPE,
        "redirect_uri": SPOTIFY_REDIRECT_URL,
        "show_dialog": "true",
    }

    url = "https://accounts.spotify.com/authorize?" + urlencode(parameters)

    return url

def callback_helper(
    code: str
):
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URL,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }

    url = "https://accounts.spotify.com/api/token"
    response = requests.post(url, data=payload)
    user_token_data = response.json()

    return user_token_data

def get_spotify_user_account_helper(
    spotfiy_access_token: str = Header(...)
):
    headers = {
        "Authorization": f"Bearer {spotfiy_access_token}"
    }

    response = requests.get(
        "https://api.spotify.com/v1/me",
        headers = headers
    )

    return response.json()

def create_spotify_playlist_helper(
    playlist_name: str,
    spotfiy_access_token: str = Header(...)        
):
    headers = {
        "Authorization": f"Bearer {spotfiy_access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": playlist_name,
        "description": "Testing Spotify API",
        "public": False
    }

    response = requests.post(
        "https://api.spotify.com/v1/me/playlists",
        headers = headers,
        json = payload
    )

    return response.json()

def get_spotify_playlist_id_helper(
    spotfiy_access_token: str = Header(...)
):
    headers = {
        "Authorization": f"Bearer {spotfiy_access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(
        "https://api.spotify.com/v1/me/playlists",
        headers = headers,
    )

    return response.json()

def get_spotify_uri_helper(
    query_song_name: str,
    spotfiy_access_token: str = Header(...)
):
    headers = {
        "Authorization": f"Bearer {spotfiy_access_token}",
        "Content-Type": "application/json"
    }

    params = {
        "q": query_song_name,
        "type": "track",
        "limit": 1
    }

    response = requests.get(
        "https://api.spotify.com/v1/search",
        headers = headers,
        params = params
    )

    return response.json()

def add_songs_to_spotify_playlist_helper(
    spotify_playlist_id: str,
    spotify_song_track_URI_obj: SpotifySongURI = Body(...),
    spotfiy_access_token: str = Header(...)
):
    headers = {
        "Authorization": f"Bearer {spotfiy_access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "uris": spotify_song_track_URI_obj.track_uris
    }

    response = requests.post(
        f"https://api.spotify.com/v1/playlists/{spotify_playlist_id}/tracks",
        headers = headers,
        json = payload
    )

    return response.json()

def get_genres_of_songs(
    spotify_song_track_URI_obj: SpotifySongURI = Body(...),
    spotfiy_access_token: str = Header(...)
):
    headers = {
        "Authorization": f"Bearer {spotfiy_access_token}",
        "Content-Type": "application/json"
    }

    results = list()

    for track_uri in spotify_song_track_URI_obj.track_uris:
        track_id = track_uri.split(":")[-1]

        track_response = requests.get(
            f"https://api.spotify.com/v1/tracks/{track_id}",
            headers = headers,
        ).json()

        artist_id = track_response["artists"][0]["id"]

        artist_response = requests.get(
            f"https://api.spotify.com/v1/artists/{artist_id}",
            headers=headers
        ).json()


        results.append({
            "genres": artist_response.get("genres", [])
        })