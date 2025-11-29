const backendURL = "http://127.0.0.1:8000/youtube_playlist_id"; 
// Custom sleep function
function sleep(ms: number): Promise<void> {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

// Home page animations upon loading
window.addEventListener("load", async () => {
    console.log("Testing testing");
    await sleep(1600);
    document.querySelector("#harmoniXfer-title")!.classList.add("animate");
    document.querySelector("#harmoniXfer-caption")!.classList.add("animate");
    document.querySelector("#transfer-song-button")!.classList.add("animate");
    document.querySelector("#title-caption-button")!.classList.add("animate");

    await sleep(900);
    document.querySelector("#image")!.classList.add("appear-fade-in");
});

// Transfer button(gets titles of YouTube videos for now)
window.addEventListener("DOMContentLoaded", () => {
    function qs<T extends HTMLElement>(selector: string): T {
        const el = document.querySelector(selector);
        if (!el) throw new Error(`Element not found: ${selector}`);
        return el as T;
    }

    const inputTextBox = qs<HTMLInputElement>("#youtube_playlist_id_1")!;
    const button = qs<HTMLButtonElement>("#youtube_to_spotify_button")!;

    button?.addEventListener("click", () => {
        const user_input = inputTextBox.value;
        console.log("user tpyed in box", user_input);

        get_youtube_playlist_video_title(user_input);
    });
});

async function get_youtube_playlist_video_title(user_input: string) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/youtube_playlist_id/${user_input}`);

        if (!response.ok) {
        throw new Error("Network response was not ok");
        }

        const data = await response.json();  // <-- Convert FastAPI JSON to JS object
        console.log("Items from backend:", data);
    } catch(error) {
        console.error("Error fetching items:", error);
    }
}
