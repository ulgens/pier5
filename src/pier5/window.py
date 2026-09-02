from .protocols import ProcessingJavaSketch


class WindowMixin:
    # Following empty variables are for typing purposes,
    # and will be assigned on the main class.
    _instance: ProcessingJavaSketch
    is_ready: bool
    uid: str

    def __init__(self) -> None:
        super().__init__()

        # py5 / Processing has no way to access the existing title.
        # Initializing the class with the default value.
        self._window_title = "Sketch"

    @property
    def window_title(self) -> str:
        return self._window_title

    @window_title.setter
    def window_title(self, value: str) -> None:
        self._window_title = value

        # windowTitle requires an active surface, which only exists once the sketch is running.
        if not self.is_ready:
            self._instance.windowTitle(self._window_title)
