import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
print(API_KEY)

YOUTUBE = build("youtube", "v3", developerKey=API_KEY)
print(YOUTUBE)

playlist_id = "PLVultSzIpDeddhF35wB1WHtuaH_rSdbks"