import os
from dotenv import load_dotenv

# Get Spotify API key
load_dotenv()
API_KEY = os.getenv("SPOTIFY_API_KEY")