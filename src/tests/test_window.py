from unittest.mock import MagicMock

from faker import Faker

from pier5 import BaseSketch

fake = Faker()


def test_default_window_title() -> None:
    """
    All sketches should have the default "Sketch" window title,
    as Processing has no way to read the existing one.
    """

    sketch = BaseSketch()

    assert sketch._window_title == "Sketch"
    assert sketch.window_title == "Sketch"


def test_window_title_getter() -> None:
    """
    Sketch.window_title should work as getter and return ._window_title
    Because Processing doesn't have any interface to return window title,
    no internal calls are made.
    """

    sketch = BaseSketch()

    assert sketch.window_title == sketch._window_title


def test_window_title_setter() -> None:
    """
    Setting Sketch.window_title should update ._window_title
    """

    sketch = BaseSketch()
    title = fake.catch_phrase()

    sketch.window_title = title

    assert sketch._window_title == title
    assert sketch.window_title == title


def test_window_title_setter_internal_call() -> None:
    """
    Setting Sketch.window_title should call _instance.windowTitle(value)
    """

    sketch = BaseSketch()
    sketch._instance = MagicMock()
    title = fake.catch_phrase()

    sketch.window_title = title

    sketch._instance.windowTitle.assert_called_once_with(title)


def test_window_title_getter_does_not_call_instance() -> None:
    """
    Accessing Sketch.window_title should only return the cached value
    without calling the Java-side instance.
    """

    sketch = BaseSketch()
    sketch._instance = MagicMock()

    sketch.window_title  # noqa: B018

    sketch._instance.assert_not_called()
