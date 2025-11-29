import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Get Youtube API key
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE = build("youtube", "v3", developerKey=API_KEY)

# Get Youtube video titles from a selected playlist
def get_playlist_videos_title(playlist_id):
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