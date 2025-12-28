"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
const backendURL = "http://127.0.0.1:8000/youtube_playlist_id";
// Custom sleep function
function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}
// Home page animations upon loading webpage
window.addEventListener("load", () => __awaiter(void 0, void 0, void 0, function* () {
    // Slide left animations
    console.log("Testing testing");
    yield sleep(1600);
    document.querySelector("#harmoniXfer-title").classList.add("animate");
    document.querySelector("#harmoniXfer-caption").classList.add("animate");
    document.querySelector("#transfer-song-button").classList.add("animate");
    document.querySelector("#title-caption-button").classList.add("animate");
    // Fade in animations
    yield sleep(900);
    document.querySelector("#statistics").classList.add("appear-fade-in");
    document.querySelectorAll(".statistics-subarea").forEach(element => {
        element.classList.add("appear-fade-in");
    });
    document.querySelectorAll(".statistics-grid-subarea").forEach(element => {
        element.classList.add("appear-fade-in");
    });
}));
function getStatisticsFromDatabase() {
    return __awaiter(this, void 0, void 0, function* () {
        const response = yield fetch("http://127.0.0.1:8000/database");
        const data = yield response.json();
        return data;
    });
}
window.addEventListener("load", () => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const statisticsData = yield getStatisticsFromDatabase();
        const songTransfered = document.getElementById('songs-transfered');
        const playlistTransfered = document.getElementById('playlists-transfered');
        const timeSaved = document.getElementById('time-saved');
        const avgTransferTime = document.getElementById('avg-transfer-time');
        songTransfered.textContent = statisticsData.total_songs_transferred_field.toString();
        playlistTransfered.textContent = statisticsData.total_playlists_transferred_field.toString();
        const minutesSavedInt = Math.floor(statisticsData.total_time_saved_field / 60);
        const secondsSavedInt = Math.floor(statisticsData.total_time_saved_field % 60);
        timeSaved.textContent = minutesSavedInt.toString() + "m " + secondsSavedInt.toString() + "s";
        const avgMinutesSavedInt = Math.floor(statisticsData.avg_time_per_song_field / 60);
        const avgSecondsSavedInt = Math.floor(statisticsData.avg_time_per_song_field % 60);
        avgTransferTime.textContent = avgMinutesSavedInt.toString() + "m " + avgSecondsSavedInt.toString() + "s";
    }
    catch (error) {
        console.error("Error fetching database data:", error);
    }
}));
// Transfer button(gets titles of YouTube videos for now)
window.addEventListener("DOMContentLoaded", () => {
    function qs(selector) {
        const el = document.querySelector(selector);
        if (!el)
            throw new Error(`Element not found: ${selector}`);
        return el;
    }
    const youtubeInputTextBox = qs("#youtube_playlist_id_1");
    const spotifyInputTextBox = qs("#spotify_playlist_id_1");
    const button = qs("#youtube_to_spotify_button");
    button === null || button === void 0 ? void 0 : button.addEventListener("click", () => {
        window.location.href = "http://127.0.0.1:8000/spotify";
    });
    button === null || button === void 0 ? void 0 : button.addEventListener("click", () => {
        const youtubeUserInput = youtubeInputTextBox.value;
        const spotifyUserInput = spotifyInputTextBox.value;
        console.log("user typed in box", youtubeUserInput);
        console.log("user typyed in box", spotifyUserInput);
        // get_youtube_playlist_video_title(youtubeUserInput);
        transfer_songs_from_youtube_to_spotify(youtubeUserInput, spotifyUserInput);
    });
});
function get_youtube_playlist_video_title(user_input) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const response = yield fetch(`http://127.0.0.1:8000/youtube_playlist_id/${user_input}`);
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            const data = yield response.json(); // Convert FastAPI JSON to JS object
            console.log("Items from backend:", data);
        }
        catch (error) {
            console.error("Error fetching items:", error);
        }
    });
}
function transfer_songs_from_youtube_to_spotify(youtubeUserInput, spotifyUserInput) {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const response = yield fetch(`http://127.0.0.1:8000/youtube-to-spotify`, {
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
            const data = yield response.json(); // Convert FastAPI JSON to JS object
            console.log("Items from backend:", data);
        }
        catch (error) {
            console.error("Error fetching items:", error);
        }
    });
}
// Clicking button scrols into song transfer area
const scrollButton = document.getElementById("transfer-song-button");
const targetSection = document.getElementById("transfer-songs-area");
scrollButton === null || scrollButton === void 0 ? void 0 : scrollButton.addEventListener("click", () => {
    targetSection === null || targetSection === void 0 ? void 0 : targetSection.scrollIntoView({ behavior: "smooth" });
});
//# sourceMappingURL=main.js.map