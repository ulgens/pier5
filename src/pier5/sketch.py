from py5 import Sketch as py5Sketch
from py5.mixins import (
    DataMixin,
    MathMixin,
    PixelMixin,
    PrintlnStream,
    ThreadsMixin,
)

from .graphics import SizeMixin
from .lifecycle import LoopMixin
from .math import RandomMixin

__all__ = ("BaseSketch",)


# Create a pure version of the py5's Sketch.
# This approach provides an easier way to eliminate unwanted mixins - behaviours.
py5Sketch.__bases__ = tuple(base for base in py5Sketch.__bases__ if base.__name__ == "Py5Base")


class BaseSketch(
    LoopMixin,
    SizeMixin,
    RandomMixin,
    MathMixin,
    DataMixin,
    ThreadsMixin,
    PixelMixin,
    PrintlnStream,
    py5Sketch,
):
    def __init__(self, *args, **kwargs) -> None:
        self.uid = f"{type(self).__name__}@0x{id(self):x}"

        super().__init__(*args, **kwargs)
