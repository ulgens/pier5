from .random import RandomMixin

__all__ = ("RandomMixin",)

# Differences against py5:
# * degrees(): numppy.degrees() wrapper
# * radians(): numpy.radians() wrapper
# * sq(): Too simple. Use "value ** 2" instead.
# * sqrt(): Too simple. Use "value ** 1/2" instead.
# * hex_color(): Use matplotlib.to_hex() instead.
# * dist() split into dist_2d() and dist_3d().
