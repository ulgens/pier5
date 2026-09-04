import warnings
from unittest.mock import MagicMock, PropertyMock

from faker import Faker
from pytest import mark

from pier5 import BaseSketch

faker = Faker()

default_dimensions = {
    "width": 100,
    "height": 100,
}


def test_default_dimensions() -> None:
    """
    All sketches start with default width and height of 100.

    > If size() is not used, the window will be given a default size of 100 x 100 pixels.
    https://processing.org/reference/size_.html
    """

    sketch = BaseSketch()

    assert sketch.width == 100
    assert sketch.height == 100


def test_width_getter() -> None:
    """
    .width's return value should be equal to ._width and ._instance.width
    """

    sketch = BaseSketch()

    assert sketch.width == sketch._width
    assert sketch.width == sketch._instance.width


def test_width_getter_internal_call() -> None:
    """
    Accessing .width should call _instance.width
    """

    sketch = BaseSketch()
    sketch._instance = MagicMock()

    # TODO: Can this mocking logic be simplified?
    mock_width = PropertyMock()
    type(sketch._instance).width = mock_width

    sketch.width  # noqa: B018
    mock_width.assert_called_once()


# Because .size() can be called only from .settings(),
# and the sketch can only be run as blocking (under macOS),
# setting the size presents a unique challenge and the only workaround I could find so far
# is to export the sketch to an image file, and then measuring its size.
# This will be implemented later.
@mark.skip(reason="TODO")
def test_width_setter() -> None: ...


def test_width_setter_internal_call() -> None:
    """
    Assigning to .width should call _instance.size() with the assigned value
    """

    sketch = BaseSketch()
    sketch._instance = MagicMock()
    new_width = faker.pyint()

    sketch.width = new_width

    sketch._instance.size.assert_called_once_with(
        new_width,
        default_dimensions["height"],
    )


def test_height_getter() -> None:
    """
    .height's return value should be equal to ._height and ._instance.height
    """

    sketch = BaseSketch()

    assert sketch.height == sketch._height
    assert sketch.height == sketch._instance.height


def test_height_getter_internal_call() -> None:
    """
    Accessing .height should call _instance.width
    """

    sketch = BaseSketch()
    sketch._instance = MagicMock()

    # TODO: Can this mocking logic be simplified?
    mock_height = PropertyMock()
    type(sketch._instance).height = mock_height

    sketch.height  # noqa: B018
    mock_height.assert_called_once()


# Because .size() can be called only from .settings(),
# and the sketch can only be run as blocking (under macOS),
# setting the size presents a unique challenge and the only workaround I could find so far
# is to export the sketch to an image file, and then measuring its size.
# This will be implemented later.
@mark.skip(reason="TODO")
def test_height_setter() -> None: ...


def test_height_setter_internal_call() -> None:
    """
    Assigning to .height should call _instance.size() with the assigned value
    """

    sketch = BaseSketch()
    sketch._instance = MagicMock()
    new_height = faker.pyint()

    sketch.height = new_height

    sketch._instance.size.assert_called_once_with(
        default_dimensions["width"],
        new_height,
    )


def test_deprecated_size_method() -> None:
    """
    Sketch.size() is deprecated.
    It should set ._width and ._height, call _instance.size() and raise a DeprecationWarning
    """
    sketch = BaseSketch()
    sketch._instance = MagicMock()

    new_width = faker.pyint()
    new_height = faker.pyint()

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        sketch.size(new_width, new_height)  # ty: ignore[deprecated]
        assert len(w) == 1

        deprecation_warning = w[0]
        assert issubclass(deprecation_warning.category, DeprecationWarning)
        assert (
            str(deprecation_warning.message)
            == "`.size(width, height)` is deprecated. Use `.width = width` and `.height = height` instead."
        )

    assert sketch._width == new_width
    assert sketch._height == new_height

    sketch._instance.size.assert_called_once_with(
        new_width,
        new_height,
    )
