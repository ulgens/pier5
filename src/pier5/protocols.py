from typing import Protocol

__all__ = ("ProcessingJavaSketch",)


class ProcessingJavaSketch(Protocol):
    """
    Structural contract for the Java-side `py5.core.Sketch` instance.

    py5 declares it as a JPype `JClass` value rather than a Python type, so the
    methods can't be imported as a type annotation. This Protocol captures the
    slice that LoopMixin actually uses.
    """

    # LoopMixin
    def isLooping(self) -> bool:  # noqa: N802
        # No official docs yet: https://github.com/processing/processing-website/issues/703
        ...

    def loop(self) -> None:
        # https://processing.org/examples/loop.html
        ...

    def noLoop(self) -> None:  # noqa: N802
        # https://processing.org/examples/noloop.html
        ...

    # / LoopMixin

    # WindowMixin
    def windowTitle(self, value: str) -> None: ...  # noqa: N802

    # / WindowMixin
