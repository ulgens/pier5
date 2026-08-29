from typing import Protocol

__all__ = ("LoopableInstance",)


class LoopableInstance(Protocol):
    """
    Structural contract for the Java-side `py5.core.Sketch` instance.

    py5 declares it as a JPype `JClass` value rather than a Python type, so the
    methods can't be imported as a type annotation. This Protocol captures the
    slice that LoopMixin actually uses.
    """

    def isLooping(self) -> bool:  # noqa: N802
        # No official docs yet: https://github.com/processing/processing-website/issues/703
        ...

    def loop(self) -> None:
        # https://processing.org/examples/loop.html
        ...

    def noLoop(self) -> None:  # noqa: N802
        # https://processing.org/examples/noloop.html
        ...
