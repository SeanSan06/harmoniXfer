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
// Custom sleep function
function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}
// Home page animations upon loading
window.addEventListener("load", () => __awaiter(void 0, void 0, void 0, function* () {
    console.log("Testing testing");
    yield sleep(1600);
    document.querySelector("#harmoniXfer-title").classList.add("animate");
    document.querySelector("#harmoniXfer-caption").classList.add("animate");
    document.querySelector("#transfer-song-button").classList.add("animate");
    document.querySelector("#title-caption-button").classList.add("animate");
    yield sleep(900);
    document.querySelector("#image").classList.add("appear-fade-in");
}));
// Transfer button(gets titles of YouTube videos for now)
window.addEventListener("DOMContentLoaded", () => {
    function qs(selector) {
        const el = document.querySelector(selector);
        if (!el)
            throw new Error(`Element not found: ${selector}`);
        return el;
    }
    const inputTextBox = qs("#youtube_playlist_id_1");
    const button = qs("#youtube_to_spotify_button");
    button === null || button === void 0 ? void 0 : button.addEventListener("click", () => {
        const text = inputTextBox.value;
        console.log("user tpyed in box", text);
    });
});
//# sourceMappingURL=main.js.map