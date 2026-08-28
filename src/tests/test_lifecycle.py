import warnings
from unittest.mock import MagicMock

from pier5 import Sketch


def test_is_looping() -> None:
    sketch = Sketch()

    # The default value is True
    assert sketch.is_looping is True
    assert sketch.is_looping == sketch._instance.isLooping()

    # Stop the loop
    sketch.is_looping = False

    assert sketch.is_looping == sketch._instance.isLooping()

    # Run the loop again
    sketch.is_looping = True
    assert sketch.is_looping == sketch._instance.isLooping()


def test_is_looping_getter_internal_call() -> None:
    """
    Accessing Sketch.is_looping should call _instance.isLooping()
    """

    sketch = Sketch()
    sketch._instance = MagicMock()

    sketch.is_looping  # noqa: B018
    sketch._instance.isLooping.assert_called_once()


def test_is_looping_setter_true_internal_call() -> None:
    """
    Setting Sketch.is_looping = True should call _instance.loop()
    """
    sketch = Sketch()
    sketch._instance = MagicMock()

    sketch.is_looping = True

    sketch._instance.loop.assert_called_once()
    sketch._instance.noLoop.assert_not_called()


def test_is_looping_setter_false() -> None:
    """
    Setting Sketch.is_looping = False should call _instance.noLoop()
    """

    sketch = Sketch()
    sketch._instance = MagicMock()

    sketch.is_looping = False

    sketch._instance.noLoop.assert_called_once()
    sketch._instance.loop.assert_not_called()


def test_deprecated_loop_method() -> None:
    """
    Sketch.loop() is deprecated.
    It should set is_looping = True and raise a DeprecationWarning.
    """

    sketch = Sketch()
    # Setting to the opposite state so the change can be tested.
    sketch.is_looping = False

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        sketch.loop()  # ty: ignore[deprecated]
        assert len(w) == 1

        deprecation_warning = w[0]
        assert issubclass(deprecation_warning.category, DeprecationWarning)
        assert str(deprecation_warning.message) == "`.loop()` is deprecated. Use `.is_looping = True` instead."

    assert sketch.is_looping is True


def test_deprecated_no_loop_method() -> None:
    """
    Sketch.no_loop() is deprecated.
    It should set is_looping = False and raise a DeprecationWarning.
    """

    sketch = Sketch()
    # Setting to the opposite state so the change can be tested.
    sketch.is_looping = True

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        sketch.no_loop()  # ty: ignore[deprecated]
        assert len(w) == 1

        deprecation_warning = w[0]
        assert issubclass(deprecation_warning.category, DeprecationWarning)
        assert str(deprecation_warning.message) == "`.no_loop()` is deprecated. Use `.is_looping = False` instead."

    assert sketch.is_looping is False
