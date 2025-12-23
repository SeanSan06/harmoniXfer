import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import re
from typing import List

# Get Youtube API key
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE = build("youtube", "v3", developerKey=API_KEY)

# Get Youtube video titles from a selected playlist
def get_playlist_videos_title(playlist_id: List[str]) -> List[str]:
    videos = []
    next_page = None

    while True:
        response = YOUTUBE.playlistItems().list(
            part = "snippet",
            playlistId = playlist_id,
            maxResults = 5,
            pageToken = next_page
        ).execute()

        for item in response["items"]:
            title = item["snippet"]["title"]
            video_id = item["snippet"]["resourceId"]["videoId"]
            videos.append((title, video_id))

        next_page = response.get("nextPageToken")
        if not next_page:
            break

    return videos

# Uses regex to clean titles
def parse_video_titles(song_titles_list: List[str]) -> List[str]:
    junk_phrases = [
        "official video",
        "official music video",
        "official hd video",
        "official hd music",
        "official hd music video",
        "official music",
        "official audio",
        "official lyric",
        "official lyrics",
        "official lyric video",
        "audio",
        "audios",
        "lyric",
        "lyrics",
        "lyric video",
        "lyric audio",
        "audio music",
        "official audio",
        "music audio",
        "audio visualizer",
        "4k video",
        "4k music video",
        "official 4k music video",
    ]

    cleaned_titles = []

    def clean_title(song_title: str) -> str:
        title = re.sub("\/()[]^*", "", title)

        for phrase in junk_phrases:
            title = re.sub(phrase, "", title, flags = re.IGNORECASE)

        return " ".join(title.split())
    
    return [clean_title(song_title) for song_title in song_titles_list]