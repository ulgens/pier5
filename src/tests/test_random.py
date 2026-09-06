import random
import warnings
from unittest.mock import MagicMock

import numpy as np
from faker import Faker

from pier5 import BaseSketch

faker = Faker()


def test_default_seed() -> None:
    """
    All sketches should have an integer seed by default.
    """

    sketch = BaseSketch()

    assert sketch._seed
    assert isinstance(sketch._seed, int)


def test_seed_getter() -> None:
    """
    Accessing .seed should return _seed
    """

    sketch = BaseSketch()

    # Validate .seed returns ._seed
    assert sketch.seed == sketch._seed


def test_seed_setter_base() -> None:
    """
    Assigning to .seed should update ._seed
    """

    sketch = BaseSketch()

    # Validate ._seed is updated
    old_seed = sketch._seed
    new_seed = random.Random().getrandbits(32)  # noqa: S311

    sketch.seed = new_seed

    assert sketch._seed != old_seed
    assert sketch._seed == new_seed


def test_seed_setter_random() -> None:
    """
    Assigning to .seed should update .rng
    """

    sketch = BaseSketch()
    new_seed = random.Random().getrandbits(32)  # noqa: S311
    sketch.seed = new_seed

    # Validate sketch.rng is default_rng(new_seed)
    expected_rng = np.random.default_rng(new_seed)
    assert sketch.rng.random() == expected_rng.random()

    # Validate ._rng is in sync with .rng
    assert sketch._rng is sketch.rng


def test_seed_setter_noise() -> None:
    """
    Assigning to .seed should call ._instance.noiseSeed()
    """

    sketch = BaseSketch()
    sketch._instance = MagicMock()

    new_seed = random.Random().getrandbits(32)  # noqa: S311
    sketch.seed = new_seed

    sketch._instance.noiseSeed.assert_called_once_with(new_seed)


def test_seed_setter_os_noise() -> None:
    """
    Assigning to .seed should call ._instance.osNoiseSeed()
    """

    sketch = BaseSketch()
    sketch._instance = MagicMock()

    new_seed = random.Random().getrandbits(32)  # noqa: S311
    sketch.seed = new_seed

    sketch._instance.osNoiseSeed.assert_called_once_with(new_seed)


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


def test_deprecated_noise_seed_method() -> None:
    """
    Sketch.noise_seed() is deprecated.
    It should work as .seed setter, but also raise a DeprecationWarning
    """

    sketch = BaseSketch()
    new_seed = random.Random().getrandbits(32)  # noqa: S311

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        sketch.noise_seed(new_seed)  # ty: ignore[deprecated]
        assert len(w) == 1

        deprecation_warning = w[0]
        assert issubclass(deprecation_warning.category, DeprecationWarning)
        depr_msg = (
            "`.noise_seed(value)` is deprecated. Use `.seed = value` instead. "
            "pier5 uses a single seed for random, noise and os_noise. "
            "Calling the deprecated .noise_seed() will update all of them."
        )
        assert str(deprecation_warning.message) == depr_msg

    assert sketch.seed == new_seed


def test_deprecated_os_noise_seed_method() -> None:
    """
    Sketch.noise_seed() is deprecated.
    It should work as .seed setter, but also raise a DeprecationWarning
    """

    sketch = BaseSketch()
    new_seed = random.Random().getrandbits(32)  # noqa: S311

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        sketch.os_noise_seed(new_seed)  # ty: ignore[deprecated]
        assert len(w) == 1

        deprecation_warning = w[0]
        assert issubclass(deprecation_warning.category, DeprecationWarning)
        depr_msg = (
            "`.os_noise_seed(value)` is deprecated. Use `.seed = value` instead. "
            "pier5 uses a single seed for random, noise and os_noise. "
            "Calling the deprecated .os_noise_seed() will update all of them."
        )
        assert str(deprecation_warning.message) == depr_msg

    assert sketch.seed == new_seed


def test_noise_detail() -> None:
    """
    .noise_detail(lod=val1, falloff=val2) should call ._instance.noiseDetail(val1, val2)
    """

    sketch = BaseSketch()
    sketch._instance = MagicMock()

    lod_value = faker.pyint()
    falloff_value = faker.pyfloat()

    sketch.noise_detail(lod=lod_value, falloff=falloff_value)

    sketch._instance.noiseDetail.assert_called_once_with(
        lod_value,
        falloff_value,
    )


# TODO:
#   Add tests for RandomMixin.random*() methods
#   https://github.com/ulgens/pier5/issues/36


# TODO: Add tests for RandomMixin.*noise*() methods
