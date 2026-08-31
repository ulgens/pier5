from typing import Any

from typing_extensions import deprecated

from pier5.protocols import ProcessingJavaSketch

__all__ = ("SizeMixin", "SizeModificationError")


class SizeModificationError(RuntimeError):
    """Raised when a settings-only size operation is called after the sketch starts running."""

    def __init__(self, method: str) -> None:
        message = (
            f"Cannot change the window size in `{method}()`. Do this in `__init__()` or "
            "`settings()`, before the sketch starts running."
        )
        super().__init__(message)


class SizeMixin:
    """
    Size-related logic for sketch dimensions.

    ``width`` and ``height`` are settable properties backed directly by the Java
    sketch's own ``width``/``height`` fields, so pier5 keeps no secondary state for
    them. Assigning to them buffers the initial size before the sketch runs and resizes
    the window afterwards.

    Alternatively, call ``full_screen()`` to open the sketch in full-screen mode.
    ``full_screen()`` and ``width``/``height`` are mutually exclusive.
    """

    # Following empty variables are for typing purposes,
    # and will be assigned on the main class.
    _instance: ProcessingJavaSketch
    _py5_bridge: Any
    _full_screen_args: tuple | None = None

    def _running_method(self) -> str | None:
        bridge = getattr(self, "_py5_bridge", None)
        return bridge.current_running_method if bridge is not None else None

    def _apply_size(self, width: int, height: int) -> None:
        """Buffer the size before the window exists, otherwise resize the running window."""
        method = self._running_method()

        if method is None or method == "settings":
            # The window has not been created yet; buffer the size for settings().
            self._instance.setSize(width, height)
        else:
            # The sketch is running; resize the actual window.
            self._instance.windowResize(width, height)

    def full_screen(self, *args: Any) -> None:
        """Request a full-screen window. Call from ``__init__()`` or ``settings()``."""
        method = self._running_method()
        if method is not None and method != "settings":
            raise SizeModificationError(method)

        self._full_screen_args = args

    def settings(self) -> None:
        # size() and full_screen() are mutually exclusive and may only be called once,
        # from settings().
        # https://processing.org/reference/settings_.html
        if self._full_screen_args is not None:
            self._instance.fullScreen(*self._full_screen_args)
        else:
            self._instance.size(self.width, self.height)

    @property
    def width(self) -> int:
        return self._instance.getWidth()

    @width.setter
    def width(self, value: int) -> None:
        self._apply_size(value, self.height)

    @property
    def height(self) -> int:
        return self._instance.getHeight()

    @height.setter
    def height(self, value: int) -> None:
        self._apply_size(self.width, value)

    @deprecated("`.size(width, height)` is deprecated. Use `.width = width` and `.height = height` instead.")
    def size(self, width: int, height: int, *args, **kwargs) -> None:
        method = self._running_method()
        if method is not None and method != "settings":
            raise SizeModificationError(method)

        self._instance.size(width, height)
