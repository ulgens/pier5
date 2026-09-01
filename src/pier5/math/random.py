import logging
import random
import types
from collections.abc import Sequence
from typing import Any

import type_enforced
from numpy.random import Generator, default_rng
from typing_extensions import deprecated

from pier5.types import (
    FloatLike,
    IntLike,
)

__all__ = ("RandomMixin",)

logger = logging.getLogger(__name__)


class RandomMixin:
    """
    Randomization-related logic, values and methods.

    Keeping the randomization context on a Sketch helps to contain the context on a single Sketch instance,
    so the users can create the multiple instance of same Sketch with different seeds.
    """

    # Following empty variables are for typing purposes,
    # and will be assigned on the main class.
    uid: str

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.seed = random.Random().getrandbits(32)  # noqa: S311

    @property
    def seed(self) -> int:
        return self._seed

    # Replaces py5.Sketch.random_seed()
    @seed.setter
    def seed(self, seed: int) -> None:
        """
        Set the seed for the sketch's random number generator.

        Updating the seed reinitializes .rng with the given seed.
        """
        self._seed = seed
        self.rng: Generator = default_rng(seed)

        # Overriding existing rng to inject the new behaviour into the existing ._rng calls
        # TODO: Remove the following assignment when all ._rng calls are migrated.
        self._rng: Generator = self.rng

        # Log the new seed
        logger.info("%s seeded with %s", self.uid, seed)

    @deprecated("`.random_seed(value)` is deprecated. Use `.seed = value` instead.")
    def random_seed(self, seed: int) -> None:
        self.seed = seed

    # TODO: Add docstring for .seed

    @type_enforced.Enforcer
    def random(
        self,
        *,
        low: FloatLike = 0.0,
        high: FloatLike = 1.0,
    ) -> float:
        return self.rng.uniform(low=low, high=high)

    @type_enforced.Enforcer
    def random_int(
        self,
        *,
        low: IntLike = 0,
        high: IntLike = 1,
    ) -> int:
        return self.rng.integers(low=low, high=high, endpoint=True)

    @type_enforced.Enforcer
    def random_choice(
        self,
        seq: Sequence[Any],
    ) -> Any:
        # TODO: Contribute to upstream
        return self.rng.choice(seq)

    def random_sample(
        self,
        seq: Sequence[Any],
        size: int = 1,
        replace: bool = True,
    ) -> Sequence[Any]:
        if not len(seq):
            return []

        if isinstance(seq, types.GeneratorType):
            seq = list(seq)

        indices = self.rng.choice(
            range(len(seq)),
            size=size,
            replace=replace,
        )

        if not isinstance(seq, list):
            return seq[indices]

        return [seq[idx] for idx in indices]

    def random_permutation(self, seq: Sequence[Any]) -> Sequence[Any]:
        if isinstance(seq, types.GeneratorType):
            seq = list(seq)

        indices = self.rng.permutation(range(len(seq)))

        if not isinstance(seq, list):
            return seq[indices]

        return [seq[idx] for idx in indices]

    @type_enforced.Enforcer
    def random_gaussian(
        self,
        *,
        loc: FloatLike = 0.0,
        scale: FloatLike = 1.0,
    ):
        # TODO: Check return type
        return self.rng.normal(loc=loc, scale=scale)
