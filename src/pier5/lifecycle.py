from typing import Protocol

from typing_extensions import deprecated

__all__ = ("LoopMixin",)


class _LoopableInstance(Protocol):
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


class LoopMixin:
    _instance: _LoopableInstance

    @property
    def is_looping(self) -> bool:
        """
        Unified interface for self._instance.isLooping(), .loop() and .noLoop()

        Instead of calling 3 different methods, you can get and set .is_looping value.

        https://github.com/py5coding/py5generator/issues/789
        """
        return self._instance.isLooping()

    @is_looping.setter
    def is_looping(self, value: bool) -> None:
        if value:
            self._instance.loop()
        else:
            self._instance.noLoop()

    @deprecated("`.loop()` is deprecated. Use `.is_looping = True` instead.")
    def loop(self) -> None:
        self.is_looping = True

    @deprecated("`.no_loop()` is deprecated. Use `.is_looping = False` instead.")
    def no_loop(self) -> None:
        self.is_looping = False
