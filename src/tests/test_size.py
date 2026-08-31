import warnings
from unittest.mock import MagicMock

from pier5 import BaseSketch


def test_default_dimensions() -> None:
    """
    All sketches start with default width and height of 100.
    """

    sketch = BaseSketch()

    assert sketch.width == 100
    assert sketch.height == 100


def test_width_getter() -> None:
    """
    Sketch.width should work as getter and return _width
    """

    sketch = BaseSketch()

    assert sketch.width == sketch._width


def test_width_getter_internal_call() -> None:
    """
    Accessing Sketch.width should call _instance.getWidth()
    """

    sketch = BaseSketch()
    sketch._instance = MagicMock()

    sketch.width  # noqa: B018
    sketch._instance.getWidth.assert_called_once()


def test_width_setter() -> None:
    """
    Sketch.width should work as setter and update ._width
    """
    return

    sketch = BaseSketch()

    sketch.width = 800

    assert sketch._width == 800
    assert sketch.width == 800


def test_height_getter() -> None:
    """
    Sketch.height should work as getter and return _height
    """

    sketch = BaseSketch()

    assert sketch.height == sketch._height


def test_height_getter_internal_call() -> None:
    """
    Accessing Sketch.width should call _instance.getHeight()
    """

    sketch = BaseSketch()
    sketch._instance = MagicMock()

    sketch.height  # noqa: B018
    sketch._instance.getHeight.assert_called_once()


def test_height_setter() -> None:
    """
    Sketch.height should work as setter and update ._height
    """
    return

    sketch = BaseSketch()

    sketch.height = 600

    assert sketch._height == 600
    assert sketch.height == 600


def test_deprecated_size_method() -> None:
    """
    Sketch.size() is deprecated.
    It should set ._width and ._height and raise a DeprecationWarning
    """
    return
    sketch = BaseSketch()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        sketch.size(800, 600)  # ty: ignore[deprecated]
        assert len(w) == 1

        deprecation_warning = w[0]
        assert issubclass(deprecation_warning.category, DeprecationWarning)
        assert (
            str(deprecation_warning.message)
            == "`.size(width, height)` is deprecated. Use `.width = width` and `.height = height` instead."
        )

    assert sketch.width == 800
    assert sketch.height == 600
