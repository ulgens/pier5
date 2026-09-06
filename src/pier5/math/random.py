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
        """
        ...

        References:
        * https://processing.org/reference/randomSeed_.html
        * https://p5js.org/reference/p5/randomSeed/
        * https://py5coding.org/reference/sketch_random_seed.html
        """

        self.seed = seed

    def random(
        self,
        *,
        low,
        high,
    ):
        """
        ...

        References:
        * https://processing.org/reference/random_.html
        * https://p5js.org/reference/p5/random/
        * https://py5coding.org/reference/sketch_random.html
        """

        raise NotImplementedError

    def random_int(
        self,
        *,
        low,
        high,
    ):
        """
        ...

        References:
        * Doesn't exist in original Processing implementation
        * Doesn't exist in p5
        * https://py5coding.org/reference/sketch_random_int.html
        """

        raise NotImplementedError

    def random_choice(
        self,
        *,
        sequence,
    ):
        """
        ...

        References:
        * Doesn't exist in original Processing implementation
        * Doesn't exist in p5
        * https://py5coding.org/reference/sketch_random_choice.html
        """

        raise NotImplementedError

    def random_sample(
        self,
        *,
        sequence,
        size: int,
    ):
        """
        ...

        References:
        * Doesn't exist in original Processing implementation
        * Doesn't exist in p5
        * https://py5coding.org/reference/sketch_random_sample.html
        """

        raise NotImplementedError

    def random_permutation(
        self,
        *,
        sequence,
    ):
        """
        ...

        References:
        * Doesn't exist in original Processing implementation
        * Doesn't exist in p5
        * https://py5coding.org/reference/sketch_random_permutation.html
        """

        raise NotImplementedError

    # FIXME: Use the full word as "loc" argument name
    # TODO: Signature seems to differ from both p5 and Processing, check why.
    def random_gaussian(
        self,
        *,
        loc,
        scale,
    ):
        """
        ...

        References:
        * https://processing.org/reference/randomGaussian_
        * https://p5js.org/reference/p5/randomGaussian/
        * https://py5coding.org/reference/sketch_random_gaussian.html
        """

        raise NotImplementedError
