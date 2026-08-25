from importlib.util import find_spec

from pytest import fail


def test_sketch() -> None:
    if not find_spec("pier5.sketch"):
        fail("Can't import `BaseSketch` from the package")


def test_version() -> None:
    try:
        from pier5 import __version__
    except ImportError:
        fail("Can't import `__version__` from the package")
    else:
        assert __version__ == "0.1.0"


# https://docs.pytest.org/en/stable/#a-quick-example
def inc(x):
    return x + 1


def test_answer():
    assert inc(3) == 4


def test_sketch_mro_excludes_math_mixin() -> None:
    from pier5.sketch import BaseSketch

    mro_names = [c.__name__ for c in BaseSketch.__mro__]

    assert "MathMixin" not in mro_names
    assert not hasattr(BaseSketch, "sin")
    assert not hasattr(BaseSketch, "np_random")
    assert hasattr(BaseSketch, "run_sketch")
