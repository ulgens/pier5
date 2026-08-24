from importlib.util import find_spec

from pytest import fail


def test_sketch() -> None:
    if not find_spec("pier5.sketch"):
        fail("Can't import `Sketch` from the package")


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
