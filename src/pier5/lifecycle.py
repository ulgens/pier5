from typing_extensions import deprecated

from pier5.protocols import ProcessingJavaSketch

__all__ = ("LoopMixin",)


class LoopMixin:
    _instance: ProcessingJavaSketch

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
