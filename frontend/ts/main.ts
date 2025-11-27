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
        const text = inputTextBox.value;
        console.log("user tpyed in box", text);
    });
});


