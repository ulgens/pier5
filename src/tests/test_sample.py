from pytest import fail


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
