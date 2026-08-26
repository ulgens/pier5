from py5 import Sketch as py5Sketch
from py5.mixins import (
    DataMixin,
    MathMixin,
    PixelMixin,
    PrintlnStream,
    ThreadsMixin,
)

__all__ = ("Sketch",)


# Create a pure version of the py5's Sketch.
# This approach provides an easier way to eliminate unwanted mixins - behaviours.
py5Sketch.__bases__ = tuple(base for base in py5Sketch.__bases__ if base.__name__ == "Py5Base")


class Sketch(
    MathMixin,
    DataMixin,
    ThreadsMixin,
    PixelMixin,
    PrintlnStream,
    py5Sketch,
): ...
