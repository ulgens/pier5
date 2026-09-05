__all__ = ("SizeModificationError",)


class SizeModificationError(RuntimeError):
    """
    Raised when a settings-only size operation is called after the sketch starts running.
    """

    def __init__(self, method: str) -> None:
        message = f"Cannot change the window size in `{method}()`. Do this in `settings()`."
        super().__init__(message)
