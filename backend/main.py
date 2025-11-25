from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"FastAPI is running"}

class YoutubeToSpotify(Event):
    name: str
    youtube_playlist_link: str

class SpotifyToYoutube(Evnet):
    name: str
    username: str
    password: str
    spotify_playlist_link: str