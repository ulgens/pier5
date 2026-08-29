import logging
import random

from numpy.random import Generator, default_rng
from typing_extensions import deprecated

__all__ = ("RandomMixin",)

logger = logging.getLogger(__name__)


class RandomMixin:
    """
    Randomization-related logic, values and methods.

    Keeping the randomization context on a Sketch helps to contain the context on a single Sketch instance,
    so the users can create the multiple instance of same Sketch with different seeds.
    """

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
        sketch_uid = f"{type(self).__name__}@0x{id(self):x}"
        logger.info("%s seeded with %s", sketch_uid, seed)

    @deprecated("`.random_seed(value)` is deprecated. Use `.seed = value` instead.")
    def random_seed(self, seed: int) -> None:
        self.seed = seed
