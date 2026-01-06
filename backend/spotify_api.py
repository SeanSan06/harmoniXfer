from pydantic import BaseModel                     # Helps with type check and type conversion
import os                                          # Get environmental variables
from dotenv import load_dotenv                     # Load the keys in the env file
from fastapi.responses import RedirectResponse     # Lets broswer know what URL to go to
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

def callback_helper(code: str):
    pass