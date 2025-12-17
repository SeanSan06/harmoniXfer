from dotenv import load_dotenv                     # Load the keys in the env file
from fastapi import FastAPI                        # Backend Framework
from fastapi.middleware.cors import CORSMiddleware # CORS header to allow specify headers only
from fastapi import Header                         # Helps format data sent to Spotify API
from fastapi.responses import FileResponse         # Send a specifc HTML, CSS, & JS file to broswer
from fastapi.responses import RedirectResponse     # Lets broswer know what URL to go to
from fastapi.staticfiles import StaticFiles        # Serves a folder's files automatically
import os                                          # Get environmental variables
from pydantic import BaseModel                     # Helps with type check and type conversion
import requests                                    # HTTP client used to make API requests(For Spotify)
from urllib.parse import urlencode                 # Helps format URLs(Spotify reqs specifc URL formats)

from backend.youtube_api import get_playlist_videos_title # My own file

""" Spotify API Set up """
load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URL = os.getenv("SPOTIFY_REDIRECT_URL")

SPOTIFY_SCOPE = "playlist-modify-private playlist-modify-public"


""" Fast API Set Up """
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


""" YouTube & Spotify Pydantic Obj Set Up """
class YoutubeToSpotify(BaseModel):
    name: str
    youtube_playlist_link: str

class SpotifyToYoutube(BaseModel):
    name: str
    username: str
    password: str
    spotify_playlist_link: str


""" Youtube API Endpoints """
@app.get("/youtube_playlist_id/{youtube_playlist_id}")
def get_youtube_playlist_video_title(youtube_playlist_id: str):
    return get_playlist_videos_title(youtube_playlist_id)


""" Spotify API Endpoints """
@app.get("/spotify")
def login_spotify():
    parameters = {
        "response_type": "code",
        "client_id": SPOTIFY_CLIENT_ID,
        "scope": SPOTIFY_SCOPE,
        "redirect_uri": SPOTIFY_REDIRECT_URL,
        "show_dialog": "true",
    }

    url = "https://accounts.spotify.com/authorize?" + urlencode(parameters)

    return RedirectResponse(url)

@app.get("/auth/callback")
def callback(code : str):
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URL,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }

    url = "https://accounts.spotify.com/api/token"
    response = requests.post(url, data=payload)
    token_data = response.json()

    return token_data

@app.get("/spotify/me")
def get_spotify_user_account(spotfiy_access_token: str = Header(...)):
    headers = {
        "Authorization": f"Bearer {spotfiy_access_token}"
    }

    response = requests.get(
        "https://api.spotify.com/v1/me",
        headers = headers
    )

    return response.json()

@app.post("/spotify/create-playlist")
def create_spotify_playlist(
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
        f"https://api.spotify.com/v1/me/playlists",
        headers = headers,
        json = payload
    )

    return response.json()


""" Serve Webpages"""
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_home():
    return FileResponse("frontend/html/index.html")