import random

from pier5 import Sketch


class ExampleSketch(Sketch):
    def settings(self) -> None:
        self._width = 800
        self._height = 600

        self.size(self._width, self._height)

    def setup(self) -> None:
        self.x = self._width / 2
        self.y = self._height / 2

        self.is_looping = False

    def draw(self) -> None:
        self.background(255)

        self.fill(80, 160, 220)
        self.no_stroke()
        self.circle(self.x, self.y, 24)

        self.fill(0)

    def mouse_dragged(self) -> None:
        self.x = self.mouse_x
        self.y = self.mouse_y

        # Redrawing on events seems to produce smoother result
        self.redraw()

    def key_pressed(self) -> None:
        if self.key == "r":
            self.x = self._width / 2
            self.y = self._height / 2

            self.redraw()

        elif self.key == "s":
            self.seed = random.Random().getrandbits(32)  # noqa: S311


if __name__ == "__main__":
    sketch = ExampleSketch()
    sketch.run_sketch()
