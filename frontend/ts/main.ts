const backendURL = "http://127.0.0.1:8000/youtube_playlist_id"; 
// Custom sleep function
function sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

// Home page animations upon loading webpage
window.addEventListener("load", async () => {
    // Slide left animations
    console.log("Testing testing");
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

// Get data from database upon loading webpage
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

    // Statisical data
    async function getStatisticsFromDatabase(): Promise<Statistics> {
        const response = await fetch("http://127.0.0.1:8000/database");
        const data: Statistics = await response.json();

        return data;
    }
    
    window.addEventListener("load", async () => {
        try {
            const statisticsData = await getStatisticsFromDatabase();
            
            const songTransfered = document.getElementById('songs-transfered');
            const playlistTransfered = document.getElementById('playlists-transfered');
            const timeSaved = document.getElementById('time-saved');
            const avgTransferTime = document.getElementById('avg-transfer-time');

            songTransfered!.textContent = statisticsData.total_songs_transferred_field.toString();
            
            playlistTransfered!.textContent = statisticsData.total_playlists_transferred_field.toString();

            const minutesSavedInt = Math.floor(statisticsData.total_time_saved_field / 60);
            const secondsSavedInt = Math.floor(statisticsData.total_time_saved_field % 60);
            timeSaved!.textContent = minutesSavedInt.toString() + "m " + secondsSavedInt.toString() + "s";

            const avgMinutesSavedInt = Math.floor(statisticsData.avg_time_per_song_field / 60);
            const avgSecondsSavedInt = Math.floor(statisticsData.avg_time_per_song_field % 60);
            avgTransferTime!.textContent = avgMinutesSavedInt.toString() + "m " + avgSecondsSavedInt.toString() + "s";
            
        } catch(error) {
            console.error("Error fetching database data:", error);
        }
    });

    // Genre data
    async function getPopularGenreFromDatabase(): Promise<PopularGenre> {
        const response = await fetch("http://127.0.0.1:8000/database-genres");
        const data: PopularGenre = await response.json();

        return data;
    }

    window.addEventListener("load", async () => {
        try {
            const genreData = await getPopularGenreFromDatabase();
            
            const popularGenre = document.getElementById('popular-genre');
            const popularTimePeriod = document.getElementById('popular-time-period');

            popularGenre!.textContent = genreData.genre_name.toString();
            
            popularTimePeriod!.textContent = genreData.genre_count.toString();
        } catch(error) {
            console.error("Error fetching database data:", error);
        }
    });

// Transfer button(gets titles of YouTube videos for now)
window.addEventListener("DOMContentLoaded", () => {
    function qs<T extends HTMLElement>(selector: string): T {
        const el = document.querySelector(selector);
        if (!el) throw new Error(`Element not found: ${selector}`);
        return el as T;
    }

    const youtubeInputTextBox = qs<HTMLInputElement>("#youtube_playlist_id_1")!;
    const spotifyInputTextBox = qs<HTMLInputElement>("#spotify_playlist_id_1")!;
    const button = qs<HTMLButtonElement>("#youtube_to_spotify_button")!;

    button?.addEventListener("click", () => {
        window.location.href = "http://127.0.0.1:8000/spotify"
    });


    button?.addEventListener("click", () => {
        const youtubeUserInput = youtubeInputTextBox.value;
        const spotifyUserInput = spotifyInputTextBox.value;
        console.log("user typed in box", youtubeUserInput);
        console.log("user typyed in box", spotifyUserInput);

        // get_youtube_playlist_video_title(youtubeUserInput);
        transfer_songs_from_youtube_to_spotify(youtubeUserInput, spotifyUserInput);
    });
});

async function get_youtube_playlist_video_title(user_input: string) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/youtube_playlist_id/${user_input}`);

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json();  // Convert FastAPI JSON to JS object
        console.log("Items from backend:", data);
    } catch(error) {
        console.error("Error fetching items:", error);
    }
}

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
            })
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const data = await response.json();  // Convert FastAPI JSON to JS object
        console.log("Items from backend:", data);
    } catch(error) {
        console.error("Error fetching items:", error);
    }    
}

// Clicking button scrols into song transfer area
const scrollButton = document.getElementById("transfer-song-button") as HTMLButtonElement | null;
const targetSection = document.getElementById("transfer-songs-area") as HTMLElement | null;

scrollButton?.addEventListener("click", () => {
    targetSection?.scrollIntoView({ behavior: "smooth" });
});
