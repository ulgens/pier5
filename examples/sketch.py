import random

from pier5 import BaseSketch


class Sketch(BaseSketch):
    def __init__(self) -> None:
        super().__init__()

        self.width = 500
        self.height = 500

    def setup(self) -> None:
        self.x = self.width / 3
        self.y = self.height / 3

        self.is_looping = False

    def draw(self) -> None:
        self.background(200)

        self.fill(80, 160, 220)
        self.no_stroke()
        self.circle(self.x, self.y, 24)

        self.fill(0)

    def mouse_dragged(self) -> None:
        self.x = self.mouse_x
        self.y = self.mouse_y

        # Redrawing on events seems to produce smoother result
        self.width = 300
        self.redraw()

    def key_pressed(self) -> None:
        if self.key == "r":
            self.x = self.width / 2
            self.y = self.height / 2

            self.redraw()

        elif self.key == "s":
            self.seed = random.Random().getrandbits(32)  # noqa: S311


if __name__ == "__main__":
    sketch = Sketch()
    sketch.run_sketch()
