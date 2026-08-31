import warnings
from unittest.mock import MagicMock

from pytest import raises

from pier5 import BaseSketch
from pier5.graphics import SizeModificationError


def test_default_dimensions() -> None:
    """
    All sketches start with default width and height of 100.
    """

    sketch = BaseSketch()

    assert sketch.width == 100
    assert sketch.height == 100


def test_width_setter_buffers_before_run() -> None:
    """
    Setting .width before run_sketch() buffers the value on the Java sketch.
    """

    sketch = BaseSketch()

    sketch.width = 800

    assert sketch.width == 800
    assert int(sketch._instance.width) == 800


def test_height_setter_buffers_before_run() -> None:
    """
    Setting .height before run_sketch() buffers the value on the Java sketch.
    """

    sketch = BaseSketch()

    sketch.height = 600

    assert sketch.height == 600
    assert int(sketch._instance.height) == 600


def test_width_setter_resizes_running_window() -> None:
    """
    Setting .width while the sketch is running should resize the window.
    """

    sketch = BaseSketch()
    sketch._instance = MagicMock()
    sketch._instance.height = 100
    sketch._py5_bridge = MagicMock()
    sketch._py5_bridge.current_running_method = "draw"

    sketch.width = 800

    sketch._instance.windowResize.assert_called_once_with(800, 100)


def test_height_setter_resizes_running_window() -> None:
    """
    Setting .height while the sketch is running should resize the window.
    """

    sketch = BaseSketch()
    sketch._instance = MagicMock()
    sketch._instance.width = 100
    sketch._py5_bridge = MagicMock()
    sketch._py5_bridge.current_running_method = "draw"

    sketch.height = 600

    sketch._instance.windowResize.assert_called_once_with(100, 600)


def test_settings_applies_size() -> None:
    """
    Sketch.settings() should apply the buffered dimensions to the Java sketch once.
    """

    sketch = BaseSketch()
    sketch._instance = MagicMock()
    sketch._instance.width = 800
    sketch._instance.height = 600

    sketch.settings()

    sketch._instance.size.assert_called_once_with(800, 600)


def test_full_screen_settings() -> None:
    """
    Sketch.settings() should apply full_screen() when full-screen was requested.
    """

    sketch = BaseSketch()
    sketch._instance = MagicMock()

    sketch.full_screen()

    sketch.settings()

    sketch._instance.fullScreen.assert_called_once_with()


def test_full_screen_with_args() -> None:
    """
    Sketch.full_screen() should forward its arguments to the Java sketch.
    """

    sketch = BaseSketch()
    sketch._instance = MagicMock()

    sketch.full_screen("P2D", 2)

    sketch.settings()

    sketch._instance.fullScreen.assert_called_once_with("P2D", 2)


def test_deprecated_size_method() -> None:
    """
    Sketch.size() is deprecated.
    It should forward the call to the Java sketch and raise a DeprecationWarning.
    """

    sketch = BaseSketch()
    sketch._instance = MagicMock()

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

    sketch._instance.size.assert_called_once_with(800, 600)


def test_size_in_draw_raises() -> None:
    """
    Calling .size() after the sketch starts running should raise a meaningful error.
    """

    sketch = BaseSketch()
    sketch._py5_bridge = MagicMock()
    sketch._py5_bridge.current_running_method = "draw"

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        with raises(SizeModificationError, match="draw"):
            sketch.size(800, 600)  # ty: ignore[deprecated]


def test_full_screen_in_draw_raises() -> None:
    """
    Calling .full_screen() after the sketch starts running should raise a meaningful error.
    """

    sketch = BaseSketch()
    sketch._py5_bridge = MagicMock()
    sketch._py5_bridge.current_running_method = "draw"

    with raises(SizeModificationError, match="draw"):
        sketch.full_screen()
