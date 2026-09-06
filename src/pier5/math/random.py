import logging
import random
from collections.abc import Sequence
from types import GeneratorType
from typing import Any

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
        low: int | float = 0,
        high: int | float = 1,
    ):
        """
        ...

        References:
        * https://processing.org/reference/random_.html
        * https://p5js.org/reference/p5/random/
        * https://py5coding.org/reference/sketch_random.html
        """

        return self.rng.uniform(low=low, high=high)

    # TODO: Copying py5's behaviour here but I'm not sure about 1 as default "high" value. Revisit.
    def random_int(
        self,
        *,
        low: int = 0,
        high: int = 1,
    ):
        """
        ...

        References:
        * Doesn't exist in original Processing implementation
        * Doesn't exist in p5
        * https://py5coding.org/reference/sketch_random_int.html
        """

        # TODO: Check what does "endpoint" mean and do.
        return self.rng.integers(low=low, high=high, endpoint=True)

    # TODO: Copying py5's behaviour here but not sure how useful "Any" is. Revisit.
    def random_choice(
        self,
        *,
        sequence: Sequence[Any],
    ) -> Any | None:
        """
        ...

        References:
        * Doesn't exist in original Processing implementation
        * Doesn't exist in p5
        * https://py5coding.org/reference/sketch_random_choice.html
        """
        # The default .rng.choice() behaviour for an empty sequence is to raise an error.
        # We don't want that here, returning None is adequate.
        if not sequence:
            return None

        return self.rng.choice(sequence)

    # TODO: Copying py5's behaviour here but not sure how useful "Any" is. Revisit.
    def random_sample(
        self,
        *,
        sequence: Sequence[Any],
        size: int = 1,
        replace: bool = True,
    ) -> Sequence[Any]:
        """
        ...

        References:
        * Doesn't exist in original Processing implementation
        * Doesn't exist in p5
        * https://py5coding.org/reference/sketch_random_sample.html
        """
        # TODO: Check the original behaviour. Is the custom check necessary?
        if sequence:
            return []

        # TODO: Check the original behaviour. Is the conversion necessary?
        # TODO: Is list the best target data type here?
        # TODO: Does "GeneratorType" conforms the expected "Sequence" type?
        if isinstance(sequence, GeneratorType):
            sequence = list(sequence)

        # FIXME: It seems some Java shenanigans going on here. Make it Pythonic.
        indices = self.rng.choice(
            range(len(sequence)),
            size=size,
            replace=replace,
        )

        if not isinstance(sequence, list):
            # Not sure what's going on with typing but code is already likely to be deleted.
            return sequence[indices]  # ty: ignore[invalid-argument-type]

        return [sequence[idx] for idx in indices]

    # TODO: Copying py5's behaviour here but not sure how useful "Any" is. Revisit.
    def random_permutation(
        self,
        *,
        sequence: Sequence[Any],
    ) -> Sequence[Any]:
        """
        ...

        References:
        * Doesn't exist in original Processing implementation
        * Doesn't exist in p5
        * https://py5coding.org/reference/sketch_random_permutation.html
        """
        # TODO: Check the original behaviour. Is the conversion necessary?
        # TODO: Is list the best target data type here?
        # TODO: Does "GeneratorType" conforms the expected "Sequence" type?
        if isinstance(sequence, GeneratorType):
            sequence = list(sequence)

        # FIXME: Another set of Java shenanigans.
        indices = self.rng.permutation(range(len(sequence)))

        if not isinstance(sequence, list):
            # Not sure what's going on with typing but code is already likely to be deleted.
            return sequence[indices]  # ty: ignore[invalid-argument-type]

        return [sequence[idx] for idx in indices]

    # FIXME: Use the full word as "loc" argument name
    # TODO: Signature seems to differ from both p5 and Processing, check why.
    def random_gaussian(
        self,
        *,
        loc: int | float = 0,
        scale: int | float = 1,
    ) -> float:
        """
        ...

        References:
        * https://processing.org/reference/randomGaussian_
        * https://p5js.org/reference/p5/randomGaussian/
        * https://py5coding.org/reference/sketch_random_gaussian.html
        """

        # TODO: Check the return type
        return self.rng.normal(loc=loc, scale=scale)
