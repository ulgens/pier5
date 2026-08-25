import warnings
from functools import partial
from typing import overload

import numpy as np
import numpy.typing as npt

from pier5.types import Point2D, Point3D

__all__ = (
    "ceil",
    "constrain",
    "dist_2d",
    "dist_3d",
    "floor",
    "remap",
)


def constrain(
    amt: float | npt.NDArray,
    low: float | npt.NDArray,
    high: float | npt.NDArray,
) -> float | npt.NDArray:
    return np.where(amt < low, low, np.where(amt > high, high, amt))


def remap(
    value: float | npt.NDArray,
    start1: float | npt.NDArray,
    stop1: float | npt.NDArray,
    start2: float | npt.NDArray,
    stop2: float | npt.NDArray,
) -> float | npt.NDArray:
    denom = stop1 - start1

    # TODO: Revisit https://github.com/py5coding/py5generator/commit/20871bc4c36214ce2a2a195c274039d59c5db69a
    if denom == 0:
        warnings.warn(
            f"remap({value}, {start1}, {stop1}, {start2}, {stop2}) called, which returns NaN (not a number)",
            stacklevel=2,
        )
        return float("nan")

    return start2 + (stop2 - start2) * ((value - start1) / denom)


# TODO: Revisit arg - return type hints
def dist_2d(*, point1: Point2D, point2: Point2D):
    """
    Find distance between two points in 2D space.
    """

    return (
        sum([
            (point1.x - point2.x) ** 2,
            (point1.y - point2.y) ** 2,
        ])
        ** 0.5
    )


# TODO: Revisit arg - return type hints
def dist_3d(*, point1: Point3D, point2: Point3D):
    """
    Find distance between two points in 3D space.
    """

    return (
        sum([
            (point1.x - point2.x) ** 2,
            (point1.y - point2.y) ** 2,
            (point1.z - point2.z) ** 2,
        ])
        ** 0.5
    )


def lerp(
    start: float | npt.NDArray,
    stop: float | npt.NDArray,
    amt: float | npt.NDArray,
) -> float | npt.NDArray:
    return amt * (stop - start) + start


@overload
def mag(
    a: float | npt.NDArray,
    b: float | npt.NDArray,
    c: float | npt.NDArray = None,
) -> float:
    values = [a, b]
    if c:
        values.append(c)

    return sum([x * x for x in values]) ** 0.5


def norm(
    value: float | npt.NDArray,
    start: float | npt.NDArray,
    stop: float | npt.NDArray,
) -> float | npt.NDArray:
    return (value - start) / (stop - start)


floor = partial(np.floor, dtype=np.int64)

ceil = partial(np.ceil, dtype=np.int64)


def noise(
    x: float | npt.NDArray,
    y: float | npt.NDArray | None = None,
    z: float | npt.NDArray | None = None,
) -> float | npt.NDArray:
    self = ...
    args = (x, y, z)

    if any(isinstance(arg, np.ndarray) for arg in args):
        arrays = np.broadcast_arrays(*args)
        return np.array(self._instance.noiseArray(*[a.flatten() for a in arrays])).reshape(arrays[0].shape)

    return self._instance.noise(*args)


def os_noise(
    x: float | npt.NDArray,
    y: float | npt.NDArray | None = None,
    z: float | npt.NDArray | None = None,
    w: float | npt.NDArray | None = None,
) -> float | npt.NDArray:
    self = ...
    args = (x, y, z, w)

    if any(isinstance(arg, np.ndarray) for arg in args):
        arrays = np.broadcast_arrays(*args)
        return np.array(self._instance.osNoiseArray(*[a.flatten() for a in arrays])).reshape(arrays[0].shape)

    return self._instance.osNoise(*args)
