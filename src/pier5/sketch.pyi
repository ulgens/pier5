# TODO: Will be revisited when the Sketch is matured.

# TODO: This is wrong, we don't use the original version of the sketch.
from py5 import Sketch as _py5Sketch
from py5.mixins import (
    DataMixin,
    PixelMixin,
    PrintlnStream,
    ThreadsMixin,
)

from pier5.graphics import SizeMixin
from pier5.lifecycle import LoopMixin
from pier5.math.random import RandomMixin

py5Sketch: _py5Sketch  # noqa: N816

class BaseSketch(
    LoopMixin,
    SizeMixin,
    RandomMixin,
    DataMixin,
    ThreadsMixin,
    PixelMixin,
    PrintlnStream,
):
    def run_sketch(
        self,
        block: bool | None = None,
        *,
        py5_options: list | None = None,
        sketch_args: list | None = None,
        _osx_alt_run_method: bool = True,
    ) -> None: ...

    # FIXME: Find a way to inherit following from _py5Sketch without breaking MRO
    mouse_x: int
    mouse_y: int
    key: str
    BACKSPACE: str
    DELETE: str
    CENTER: int
    LEFT: int
    RIGHT: int
    # TODO: background() signature has 7 overloads, needs to be cleaned for a better stub.
    def background(self, *args, **kwargs) -> None: ...
    def clip(self, a: float, b: float, c: float, d: float, /) -> None: ...
    # TODO: fill() signature has 6 overloads, needs to be cleaned for a better stub.
    def fill(self, *args, **kwargs) -> None: ...
    # TODO: Signature details will be revisited.
    def line(self, *args, **kwargs) -> None: ...
    def no_clip(self) -> None: ...
    def no_stroke(self) -> None: ...
    # TODO: Signature details will be revisited.
    def rect(self, *args, **kwargs) -> None: ...
    def redraw(self): ...
    # TODO: stroke() signature has 6 overloads, needs to be cleaned for a better stub.
    def stroke(self, *args, **kwargs) -> None: ...
    # TODO: text() signature has 11 overloads, needs to be cleaned for a better stub.
    def text(self, *args, **kwargs): ...
    def text_align(self, align_x: int, align_y: int | None = None) -> None: ...
    def text_ascent(self) -> float: ...
    def text_descent(self) -> float: ...
    def text_size(self, size: float) -> None: ...
    # TODO: Signature details will be revisited.
    def text_width(self, *args, **kwargs) -> float: ...
    def window_title(self, title: str, /) -> None: ...
