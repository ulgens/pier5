float x, y;

void settings() {
    size(800, 600);
}

void setup() {
    x = width / 2.0f;
    y = height / 2.0f;

    noLoop();
}

void draw() {
    background(200);

    fill(80, 160, 220);
    noStroke();
    circle(x, y, 24);

    fill(0);
}

void mouseDragged() {
    x = mouseX;
    y = mouseY;

    redraw();
}

void keyPressed() {
    if (key == 'r') {
        x = width / 2.0f;
        y = height / 2.0f;

        redraw();
    } else if (key == 's') {
        randomSeed((long) (Math.random() * 0x100000000L));
    }
}
