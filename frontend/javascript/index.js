// Need a custom sleep function, JS doesn't have one
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Needs to gradually let each part of the page load for clean animation
window.addEventListener("load", async () => {
    await sleep(1600);
    document.querySelector("#harmoniXfer-title").classList.add("animate");
    document.querySelector("#harmoniXfer-caption").classList.add("animate");
    document.querySelector("#transfer-song-button").classList.add("animate");
    document.querySelector("#title-caption-button").classList.add("animate");

    await sleep(900);
    document.querySelector("#image").classList.add("appear-fade-in");
});