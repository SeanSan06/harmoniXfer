from fastapi import FastAPI                  # Backend Framework
from fastapi.middleware.cors import CORSMiddleware # CORS header to allow specify headers only
from fastapi.responses import FileResponse   # Send a specifc HTML, CSS, & JS file to broswer
from fastapi.staticfiles import StaticFiles  # Serves a folder's files automatically
from pydantic import BaseModel               # Helps with type check and type conversion

from backend.youtube_api import get_playlist_videos_title

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
# @app.get("/spotify")
# def home():
#     return {"Spotify API"}

# Serve Webpages
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_home():
    return FileResponse("frontend/html/index.html")