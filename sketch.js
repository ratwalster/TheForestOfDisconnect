let characters = [];
let pathX = 50;

function setup() {
    createCanvas(1280, 720).parent("app-container");
    characters = [
        { x: 50, y: 500, speed: 1, image: loadImage("lina.svg") },
        { x: 70, y: 520, speed: 1.2, image: loadImage("kai.svg") },
        { x: 90, y: 540, speed: 0.8, image: loadImage("mara.svg") },
        { x: 110, y: 560, speed: 1.1, image: loadImage("tomas.svg") },
        { x: 130, y: 580, speed: 0.9, image: loadImage("eli.svg") },
        { x: 150, y: 600, speed: 1.3, image: loadImage("sana.svg") }
    ];
}

function draw() {
    background(50, 100, 50, 150); // Misty green
    fill(255, 200, 100); noStroke(); ellipse(pathX, 600, 20); // Path glow
    characters.forEach(char => {
        char.x += char.speed;
        if (char.x > width) char.x = 50;
        image(char.image, char.x, char.y, 50, 50);
    });
    pathX += 0.5; if (pathX > width) pathX = 50;
}