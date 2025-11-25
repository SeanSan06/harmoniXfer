from fastapi import FastAPI                 # Backend Framework
from fastapi.responses import FileResponse  # Send a specifc HTML, CSS, & JS file to broswer
from fastapi.staticfiles import StaticFiles # Serves a folder's files automatically
from pydantic import BaseModel              # Helps with type check and type conversion

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
print(API_KEY)

app = FastAPI()

class YoutubeToSpotify(BaseModel):
    name: str
    youtube_playlist_link: str

class SpotifyToYoutube(BaseModel):
    name: str
    username: str
    password: str
    spotify_playlist_link: str

""" Youtube API Endpoints """
# @app.get("/youtube")
# def home():
#     return {"Youtube API"}

""" Spotify API Endpoints """
# @app.get("/spotify")
# def home():
#     return {"Spotify API"}

# Serve Webpages
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_home():
    return FileResponse("frontend/html/index.html")