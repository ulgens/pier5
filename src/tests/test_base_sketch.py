def test_py5sketch_excludes_mixins():
    """
    Base py5 Sketch shouldn't have any of the py5 mixins.
    Mixins will be added to Sketch class later, when needed.
    """

    from pier5.sketch import py5Sketch

    base_mixins = filter(lambda m: "mixin" in m.__name__.lower(), py5Sketch.__mro__)
    base_mixins = list(base_mixins)

    assert not base_mixins
