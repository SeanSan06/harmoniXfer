from collections import Counter                    # Help to count genres and place in dict
from dotenv import load_dotenv                     # Load the keys in the env file
from fastapi import FastAPI                        # Backend Framework
from fastapi.middleware.cors import CORSMiddleware # CORS header to allow specify headers only
from fastapi import Body, Header                   # Helps format data sent to Spotify API
from fastapi.responses import FileResponse         # Send a specifc HTML, CSS, & JS file to broswer
from fastapi.responses import JSONResponse         # Send JSON objs to the front-end
from fastapi.responses import RedirectResponse     # Lets broswer know what URL to go to
from fastapi.staticfiles import StaticFiles        # Serves a folder's files automatically
import math                                        # Use the celing method to round
import os                                          # Get environmental variables
from pydantic import BaseModel                     # Helps with type check and type conversion
import requests                                    # HTTP client used to make API requests(For Spotify)
from urllib.parse import urlencode                 # Helps format URLs(Spotify reqs specifc URL formats)

import backend.youtube_api as youtube              # Local file
import backend.spotify_api as spotify              # Local file
from backend.database import get_connection, create_tables, set_table_id


""" Spotify API Set up """
load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URL = os.getenv("SPOTIFY_REDIRECT_URL")

SPOTIFY_SCOPE = (
    "playlist-modify-private "
    "playlist-modify-public "
    "playlist-read-private "
    "playlist-read-collaborative"
)


""" Fast API Set Up and Database Connection"""
app = FastAPI()
create_tables()
set_table_id()
DATA_BASE = "statistics.db"

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

class SpotifySongURI(BaseModel):
    track_uris: list[str]

class YouTubeToSpotifyTransfer(BaseModel):
    youtube_playlist_id: str
    spotify_playlist_name: str


""" Youtube API Endpoints """
@app.get("/youtube_playlist_id/{youtube_playlist_id}")
def get_youtube_playlist_video_title(
    youtube_playlist_id: str
):
    return youtube.get_playlist_videos_title(youtube_playlist_id)


""" Spotify API Endpoints """
user_spotify_token = []
@app.get("/spotify")
def login_spotify():
    return RedirectResponse(spotify.login_spotify_helper())

@app.get("/auth/callback")
def callback(
    code : str
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
    
    user_spotify_token.append(user_token_data)
    
    return RedirectResponse("/")

@app.get("/spotify/me")
def get_spotify_user_account(
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
        "https://api.spotify.com/v1/me/playlists",
        headers = headers,
        json = payload
    )

    return response.json()

@app.get("/spotify/get-playlist-id")
def get_spotify_playlist_id(
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

@app.get("/spotify/get-song-uri")
def get_spotify_uri(
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

@app.post("/spotify/add-songs")
def add_songs_to_spotify_playlist(
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

@app.get("/spotify/get-genres")
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

    return results

@app.post("/youtube-to-spotify")
def youtube_to_spotify(
    YTSpfyObj: YouTubeToSpotifyTransfer
):
    youtube_playlist_id = YTSpfyObj.youtube_playlist_id
    spotify_playlist_name = YTSpfyObj.spotify_playlist_name

    yt_playlist_video_information = get_youtube_playlist_video_title(youtube_playlist_id)

    yt_songs_title_list = []
    for list_index in yt_playlist_video_information:
        yt_songs_title_list.append(list_index)

    # Get Spotify user's auth token, redirect user back to get Spotify token
    if not user_spotify_token:
        return JSONResponse(
            status_code=401,
            content={"error": "Not authenticated"}
        )
    user_spotify_token_local = user_spotify_token[0]["access_token"]

    # For each song title get its Spotify URI and avoids crashes if Spotify API finds nothing
    song_uri_list = []
    for song_title in yt_songs_title_list:
        search_response = get_spotify_uri(song_title, user_spotify_token_local)
        items = search_response["tracks"]["items"]

        if items:
            song_uri_list.append(items[0]["uri"])

    # Find the matching Spotify playlist ID given the playlist's title that user typed in
    spotify_playlist_id = ""
    all_spotify_playlist_info = get_spotify_playlist_id(user_spotify_token_local)["items"]
    for playlist_info in all_spotify_playlist_info:
        if(playlist_info["name"] == spotify_playlist_name):
            spotify_playlist_id = playlist_info["id"]

    if not spotify_playlist_id:
        return {"error": "Playlist not found"}
      
    # Place each song using its URI into the existing Spotify playlist using its playlist ID(WIP)
    add_songs_to_spotify_playlist(
        spotify_playlist_id = spotify_playlist_id,
        spotify_song_track_URI_obj = SpotifySongURI(track_uris=song_uri_list),
        spotfiy_access_token = user_spotify_token_local
    )

    # Get the genres for all songs transferred between playlists
    genres = get_genres_of_songs(
        spotify_song_track_URI_obj = SpotifySongURI(track_uris=song_uri_list),
        spotfiy_access_token = user_spotify_token_local
    )

    genre_counter = Counter()

    for item in genres:
        for genre in item["genres"]:
            genre_counter.update([genre.capitalize()])

    genre_counter = dict(genre_counter)

    # Calcualte data
    songs_transferred = len(song_uri_list)
    yt_calls = math.ceil(songs_transferred / 50)
    spotify_calls = songs_transferred + 4
    total_time_saved = (songs_transferred * 20) - (songs_transferred * 5)
    avg_time_per_song = total_time_saved/songs_transferred

    # Put data into SQLite database
    connection = get_connection()
    cursor = connection.cursor()

    ## Statistics Data
    cursor.execute(""" 
        UPDATE statistics
        SET
            total_songs_transferred_field = total_songs_transferred_field + ?,
            total_playlists_transferred_field = total_playlists_transferred_field + ?,
            total_time_saved_field = total_time_saved_field + ?
        WHERE id_field = 1
    """, (
        songs_transferred,
        1,
        total_time_saved,
    )
    )
    cursor.execute("""
        UPDATE statistics
        SET avg_time_per_song_field = 
            CASE
                WHEN total_songs_transferred_field > 0
                THEN total_time_saved_field / total_songs_transferred_field
                ELSE 0
            END
        WHERE id_field = 1
    """)

    ## Genre Data
    for genre_key, genre_value in genre_counter.items():
        cursor.execute("""
            INSERT INTO genres (genre_name, genre_count)
            VALUES (?, ?)
            ON CONFLICT(genre_name)
            DO UPDATE SET genre_count = genre_count + excluded.genre_count
        """, (
            genre_key,
            genre_value
        )
        )

    connection.commit()
    connection.close()

    # return genre_counter
    return {
        "success": (
            f"{songs_transferred} songs have been transferred!"
            f"{yt_calls} YouTube API calls made!"
            f"{spotify_calls} Spotify API calls made!"
            f"{total_time_saved} Time Saved!"
            f"{avg_time_per_song} Average Time to Transfer a Song!"
        )
    }
    # Important variables "yt_songs_title_list, user_spotify_token_local, song_uri_list, spotify_playlist_id, genre_counter"


""" Database endpoints """
@app.get("/database")
def get_values_database():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT
            total_songs_transferred_field,
            total_playlists_transferred_field,
            total_time_saved_field,
            avg_time_per_song_field
        FROM statistics
        WHERE id_field = 1
    """)
    data = cursor.fetchone()
    connection.close()
    
    return data

@app.get("/database-genres")
def get_genres_database():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT 
            genre_name,
            genre_count
        FROM genres
        ORDER BY genre_count DESC
        LIMIT 1
    """)
    genre_pair_data = cursor.fetchone()
    connection.close()
    
    return genre_pair_data


""" Serve Webpages """
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_home():
    return FileResponse("frontend/html/index.html")