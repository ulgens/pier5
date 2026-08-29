import random
import warnings

import numpy as np

from pier5 import BaseSketch


def test_default_seed() -> None:
    """
    All sketches should have an integer seed by default.
    """

    sketch = BaseSketch()

    assert sketch._seed
    assert isinstance(sketch._seed, int)


def test_seed_getter() -> None:
    """
    Sketch.seed should work as getter and return _seed
    """

    sketch = BaseSketch()

    # Validate .seed returns ._seed
    assert sketch.seed == sketch._seed


def test_seed_setter() -> None:
    """
    Sketch.seed should work as setter and update ._seed and .rng
    """

    sketch = BaseSketch()

    # Validate ._seed is updated
    old_seed = sketch._seed
    new_seed = random.Random().getrandbits(32)  # noqa: S311

    sketch.seed = new_seed

    assert sketch._seed != old_seed
    assert sketch._seed == new_seed

    # Validate sketch.rng is default_rng(new_seed)
    expected_rng = np.random.default_rng(new_seed)
    assert np.array_equal(sketch.rng.random(), expected_rng.random())

    # Validate ._rng is in sync with .rng
    assert sketch._rng is sketch.rng


def test_deprecated_random_seed_method() -> None:
    """
    Sketch.random_seed() is deprecated.
    It should work as .seed setter, but also raise a DeprecationWarning
    """

    sketch = BaseSketch()
    new_seed = random.Random().getrandbits(32)  # noqa: S311

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        sketch.random_seed(new_seed)  # ty: ignore[deprecated]
        assert len(w) == 1

        deprecation_warning = w[0]
        assert issubclass(deprecation_warning.category, DeprecationWarning)
        assert str(deprecation_warning.message) == "`.random_seed(value)` is deprecated. Use `.seed = value` instead."

    assert sketch.seed == new_seed
