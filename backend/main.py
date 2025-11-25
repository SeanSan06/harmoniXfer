from fastapi import FastAPI                 # Backend Framework
from fastapi.responses import FileResponse  # Send file to broswer
from fastapi.staticfiles import StaticFiles # Serve folder
from pydantic import BaseModel              # Helps type check

app = FastAPI()

class YoutubeToSpotify(BaseModel):
    name: str
    youtube_playlist_link: str

class SpotifyToYoutube(BaseModel):
    name: str
    username: str
    password: str
    spotify_playlist_link: str

# End points
# @app.get("/")
# def home():
#     return {"FastAPI is running"}

# Serve Webpages
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_home():
    return FileResponse("frontend/html/index.html")