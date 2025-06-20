const characters = [
    { name: "Lina", image: "lina.svg", audio: "audio/chapter_1_lina.mp3" },
    { name: "Kai", image: "kai.svg", audio: "audio/chapter_2_kai.mp3" },
    { name: "Mara", image: "mara.svg", audio: "audio/chapter_3_mara.mp3" },
    { name: "Tomas", image: "tomas.svg", audio: "audio/chapter_4_tomas.mp3" },
    { name: "Eli", image: "eli.svg", audio: "audio/chapter_5_eli.mp3" },
    { name: "Sana", image: "sana.svg", audio: "audio/chapter_6_sana.mp3" },
    { name: "Narrator", image: "narrator.svg", audio: "audio/narration_intro.mp3" }
];

characters.forEach(char => {
    const button = document.createElement("button");
    button.innerHTML = `<img src="${char.image}" alt="${char.name}">`;
    button.addEventListener("click", () => playAudio(char.audio));
    document.getElementById("character-menu").appendChild(button);
});

function playAudio(src) {
    const audio = new Audio(src);
    audio.play().catch(error => console.log("Audio play failed:", error));
}

document.querySelectorAll(".character-node").forEach(node => {
    node.addEventListener("click", () => playAudio(node.dataset.audio));
});