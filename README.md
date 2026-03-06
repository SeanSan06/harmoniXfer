# HarmoniXfer
A full stack web application that allows users to transfer songs between their Spotify and YouTube playlists automatically.

## Pictures of website
![Example Image](/frontend/images/homepage.png)

## Features
- Transfer playlists between Spotify and YouTube Music
- Real-time playlist synchronization
- Track transfer history with SQLite database

## Future features
- Use Scikit-learn to perform machine learning and recommend new songs based on playlists
- Design a dashboard that displays statistical information and song suggestions
- Clean up the color scheme for a simplistic and inviting design
- Add footer and redesign the header bar

## Setup

### Prerequisites
- Python 3.12 or higher
- Node.js and npm (for TypeScript)
- Spotify Developer Account
- YouTube API credentials

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/harmoniXfer.git
   cd harmoniXfer
   ```

2. **Set up Python virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install TypeScript**
   ```bash
   npm install -g typescript
   ```

5. **Configure environment variables**
   
   Create a `.env` file in the project root (You will need to make an developer account for each of these 2 platforms):
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   YOUTUBE_API_KEY=your_youtube_api_key
   ```

6. **Run the application**
   ```bash
   uvicorn backend.main:app --reload
   ```
   
   The API will be available at `http://127.0.0.1:8000`

7. **Deactivate the virtual environment** (when done using/testing)
   ```bash
   deactivate
   ```

## How it's made

**Technology used**: HTML, CSS, TypeScript, FastAPI, Python, SQLite, YouTube API, and Spotify API.

**HTML**: Layout structure for all web pages (Home, Song Transfer, and About sections)

**CSS**: Creates a simplistic and animated website with smooth transitions and effects

**TypeScript**: Provides dynamic functionality and frontend-backend communication

**FastAPI with Python**: Custom REST API enabling real-time communication between frontend and backend

**SQLite**: Lightweight database for storing transfer history and statistics

**YouTube API**: Retrieves playlist data and song titles from YouTube playlists

**Spotify API**: Manages Spotify playlists and adds songs based on YouTube playlist data

## What I learned

- Building type-safe frontends with TypeScript and custom objects for data transfer
- Designing animated, interactive web interfaces with CSS
- Creating scalable backend APIs with FastAPI
- Integrating multiple third-party APIs (Spotify and YouTube)
- Managing database operations with SQLite
- Implementing OAuth authentication flows

## Credits
- YouTube API and Spotify API for backend functionality
- [TISEPSE](https://uiverse.io/profile/TISEPSE) for the animated button UI
- [Cohen](https://uiverse.io/profile/cohencoo) for the animated text box input UI