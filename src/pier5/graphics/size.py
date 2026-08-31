from typing_extensions import deprecated

from ..protocols import ProcessingJavaSketch

__all__ = ("SizeMixin",)

# > If size() is not used, the window will be given a default size of 100 x 100 pixels.
# https://processing.org/reference/size_.html
DEFAULT_SIZE = {
    "width": 100,
    "height": 100,
}


class SizeMixin:
    """
    Size-related logic for sketch dimensions.

    Provides properties for accessing width and height, and manages the underlying size state.
    """

    # Following empty variables are for typing purposes,
    # and will be assigned on the main class.
    _instance: ProcessingJavaSketch

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._width: int = DEFAULT_SIZE["width"]
        self._height: int = DEFAULT_SIZE["height"]

    @property
    def width(self) -> int:
        return self._instance.getWidth()

    @width.setter
    def width(self, value: int) -> None:
        self._width = value
        self._instance.size(self._width, self._height)

    @property
    def height(self) -> int:
        return self._instance.getHeight()

    @height.setter
    def height(self, value: int) -> None:
        self._height = value
        self._instance.size(self._width, self._height)

    @deprecated("`.size(width, height)` is deprecated. Use `.width = width` and `.height = height` instead.")
    def size(self, width: int, height: int, *args, **kwargs) -> None:
        self._width = width
        self._height = height
        self._instance.size(self._width, self._height)
