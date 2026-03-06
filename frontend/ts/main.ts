// ========== CONFIGURATION ==========
const backendURL = "http://127.0.0.1:8000/youtube_playlist_id";

// ========== TYPES ==========
interface Statistics {
    total_songs_transferred_field: number;
    total_playlists_transferred_field: number;
    total_time_saved_field: number;
    avg_time_per_song_field: number;
}

interface PopularGenre {
    genre_name: string;
    genre_count: number;
}

// ========== UTILITY FUNCTIONS ==========
function sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

function qs<T extends HTMLElement>(selector: string): T {
    const el = document.querySelector(selector);
    if (!el) throw new Error(`Element not found: ${selector}`);
    return el as T;
}

// ========== ANIMATIONS ==========
window.addEventListener("load", async () => {
    console.log("Starting page animations");
    
    // Slide left animations
    await sleep(1600);
    document.querySelector("#harmoniXfer-title")!.classList.add("animate");
    document.querySelector("#harmoniXfer-caption")!.classList.add("animate");
    document.querySelector("#transfer-song-button")!.classList.add("animate");
    document.querySelector("#title-caption-button")!.classList.add("animate");

    // Fade in animations
    await sleep(900);
    document.querySelector("#statistics")!.classList.add("appear-fade-in");
    document.querySelectorAll(".statistics-subarea").forEach(element => {
        element.classList.add("appear-fade-in");
    });
    document.querySelectorAll(".statistics-grid-subarea").forEach(element => {
        element.classList.add("appear-fade-in");
    });
});

// ========== DATABASE API CALLS ==========
async function getStatisticsFromDatabase(): Promise<Statistics> {
    const response = await fetch("http://127.0.0.1:8000/database");
    const data: Statistics = await response.json();
    return data;
}

async function getPopularGenreFromDatabase(): Promise<PopularGenre> {
    const response = await fetch("http://127.0.0.1:8000/database-genres");
    const data: PopularGenre = await response.json();
    return data;
}

// ========== STATISTICS DISPLAY ==========
window.addEventListener("load", async () => {
    try {
        const statisticsData = await getStatisticsFromDatabase();
        
        // Update statistics elements
        const songTransfered = document.getElementById('songs-transfered');
        const playlistTransfered = document.getElementById('playlists-transfered');
        const timeSaved = document.getElementById('time-saved');
        const avgTransferTime = document.getElementById('avg-transfer-time');

        songTransfered!.textContent = statisticsData.total_songs_transferred_field.toString();
        playlistTransfered!.textContent = statisticsData.total_playlists_transferred_field.toString();

        // Format time saved as minutes and seconds
        const minutesSavedInt = Math.floor(statisticsData.total_time_saved_field / 60);
        const secondsSavedInt = Math.floor(statisticsData.total_time_saved_field % 60);
        timeSaved!.textContent = minutesSavedInt.toString() + "m " + secondsSavedInt.toString() + "s";

        // Format average transfer time as minutes and seconds
        const avgMinutesSavedInt = Math.floor(statisticsData.avg_time_per_song_field / 60);
        const avgSecondsSavedInt = Math.floor(statisticsData.avg_time_per_song_field % 60);
        avgTransferTime!.textContent = avgMinutesSavedInt.toString() + "m " + avgSecondsSavedInt.toString() + "s";
            
    } catch(error) {
        console.error("Error fetching statistics data:", error);
    }
});

// ========== POPULAR GENRE DISPLAY ==========
window.addEventListener("load", async () => {
    try {
        const genreData = await getPopularGenreFromDatabase();
        
        const popularGenre = document.getElementById('popular-genre');
        const popularTimePeriod = document.getElementById('popular-time-period');

        popularGenre!.textContent = genreData.genre_name.toString();
        popularTimePeriod!.textContent = genreData.genre_count.toString();
        
    } catch(error) {
        console.error("Error fetching genre data:", error);
    }
});

// ========== SONG TRANSFER FUNCTIONALITY ==========
async function transfer_songs_from_youtube_to_spotify(youtubeUserInput: string, spotifyUserInput: string) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/youtube-to-spotify`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                youtube_playlist_id: youtubeUserInput,
                spotify_playlist_name: spotifyUserInput
            }),
            redirect: "follow"
        });

        // Redirect to Spotify auth if no token exists
        if (response.status === 401) {
            window.location.href = "http://127.0.0.1:8000/spotify";
            return;
        }

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        
        const data = await response.json(); 
        console.log("Items from backend:", data);
        
    } catch(error) {
        console.error("Error transferring songs:", error);
    }    
}

window.addEventListener("DOMContentLoaded", () => {
    // Check if there's a pending transfer from before page reload
    const pending = localStorage.getItem("pendingTransfer");
    if (pending) {
        const { youtube_playlist_id, spotify_playlist_name } = JSON.parse(pending);
        localStorage.removeItem("pendingTransfer");
        transfer_songs_from_youtube_to_spotify(youtube_playlist_id, spotify_playlist_name);
    }

    // Setup transfer button click handler
    const youtubeInputTextBox = qs<HTMLInputElement>("#youtube_playlist_id_1");
    const spotifyInputTextBox = qs<HTMLInputElement>("#spotify_playlist_id_1");
    const button = qs<HTMLButtonElement>("#youtube_to_spotify_button");

    button.addEventListener("click", () => {
        const youtubeUserInput = youtubeInputTextBox.value;
        const spotifyUserInput = spotifyInputTextBox.value;
        
        console.log("YouTube input:", youtubeUserInput);
        console.log("Spotify input:", spotifyUserInput);

        // Save user input for persistence across page reloads
        localStorage.setItem("pendingTransfer", JSON.stringify({
            youtube_playlist_id: youtubeUserInput,
            spotify_playlist_name: spotifyUserInput
        }));

        transfer_songs_from_youtube_to_spotify(youtubeUserInput, spotifyUserInput);
    });
});

// ========== SCROLL FUNCTIONALITY(when clicking nav buttons) ==========
window.addEventListener("DOMContentLoaded", () => {
    const scrollButton = document.getElementById("transfer-song-button") as HTMLButtonElement | null;
    const targetSection = document.getElementById("transfer-songs-area") as HTMLElement | null;

    scrollButton?.addEventListener("click", () => {
        targetSection?.scrollIntoView({ behavior: "smooth" });
    });
});