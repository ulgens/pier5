let x, y;

function setup() {
    createCanvas(800, 600);

    x = width / 2;
    y = height / 2;

    noLoop();
}

function draw() {
    background(200);

    fill(80, 160, 220);
    noStroke();
    circle(x, y, 24);

    fill(0);
}

function mouseDragged() {
    x = mouseX;
    y = mouseY;

    redraw();
}

function keyPressed() {
    if (key === "r") {
        x = width / 2;
        y = height / 2;

        redraw();
    } else if (key === "s") {
        randomSeed(Math.floor(Math.random() * 2 ** 32));
    }
}
