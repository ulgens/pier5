from typing import Any, Protocol

__all__ = ("ProcessingJavaSketch",)


class ProcessingJavaSketch(Protocol):
    """
    Structural contract for the Java-side `py5.core.Sketch` instance.

    py5 declares it as a JPype `JClass` value rather than a Python type, so the
    methods can't be imported as a type annotation. This Protocol captures the
    slice that pier5's mixins actually use.
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

    # SizeMixin
    def getWidth(self) -> int: ...  # noqa: N802

    def getHeight(self) -> int: ...  # noqa: N802

    def setSize(self, width: int, height: int) -> None: ...  # noqa: N802

    def windowResize(self, width: int, height: int) -> None: ...  # noqa: N802

    def size(self, width: int, height: int) -> None: ...

    def fullScreen(self, *args: Any) -> None: ...  # noqa: N802

    # / SizeMixin
