# TODO: Will be revisited when the Sketch is matured.

# TODO: This is wrong, we don't use the original version of the sketch.
from py5 import Sketch as _py5Sketch
from py5.mixins import (
    DataMixin,
    MathMixin,
    PixelMixin,
    PrintlnStream,
    ThreadsMixin,
)

from pier5.math.random import RandomMixin

py5Sketch: _py5Sketch  # noqa: N816

class Sketch(
    RandomMixin,
    MathMixin,
    DataMixin,
    ThreadsMixin,
    PixelMixin,
    PrintlnStream,
): ...
