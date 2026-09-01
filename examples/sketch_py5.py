import random

import py5


class Sketch(py5.Sketch):
    def settings(self) -> None:
        self.size(800, 600)

    def setup(self) -> None:
        self.x = self.width / 2
        self.y = self.height / 2

        self.no_loop()

    def draw(self) -> None:
        self.background(200)

        self.fill(80, 160, 220)
        self.no_stroke()
        self.circle(self.x, self.y, 24)

        self.fill(0)

    def mouse_dragged(self) -> None:
        self.x = self.mouse_x
        self.y = self.mouse_y

        self.redraw()

    def key_pressed(self) -> None:
        if self.key == "r":
            self.x = self.width / 2
            self.y = self.height / 2

            self.redraw()

        elif self.key == "s":
            self.random_seed(random.getrandbits(32))


if __name__ == "__main__":
    sketch = Sketch()
    sketch.run_sketch()
