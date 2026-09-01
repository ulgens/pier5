from dataclasses import dataclass

from numpy import integer as npint
from numpy.typing import NDArray

__all__ = (
    "FloatLike",
    "IntLike",
    "Point2D",
    "Point3D",
)


IntLike = int | npint

FloatLike = IntLike | float


@dataclass
class Point2D:
    x: float | NDArray
    y: float | NDArray


@dataclass
class Point3D(Point2D):
    z: float | NDArray
