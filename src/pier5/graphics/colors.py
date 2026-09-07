from matplotlib.colors import (
    to_hex,
    to_rgba,
)

__all__ = ("Color",)


class Color:
    """
    https://processing.org/reference/color_datatype.html
    https://p5js.org/reference/#Color
    """

    # TODO:
    #   p5's color interface seems richer than Processing's:
    #   * https://p5js.org/reference/#Color

    def __init__(
        self,
        # TODO: 0-1 vs 0-255?
        red: float = 0.0,
        green: float = 0.0,
        blue: float = 0.0,
        alpha: float = 1.0,
    ):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    # RGB
    @property
    def rgb(self):
        return self.red, self.green, self.blue

    @rgb.setter
    def rgb(self, value):
        self.red, self.green, self.blue = value

    # / RGB

    # RGBA
    @property
    def rgba(self):
        return self.red, self.green, self.blue, self.alpha

    @rgba.setter
    def rgba(self, value):
        self.red, self.green, self.blue, self.alpha = value

    # / RGBA

    # Hexcode
    @classmethod
    def from_hexcode(cls, value):
        rgba = to_rgba(value)
        return cls(*rgba)

    @property
    def hexcode(self):
        # TODO: Revisit alpha handling
        return to_hex(self.rgba, keep_alpha=True)

    @hexcode.setter
    def hexcode(self, value):
        # TODO: Revisit alpha handling
        # TODO: Does to_rgba handle validation?
        self.rgba = to_rgba(value)

    # / Hexcode

    # Gray
    @classmethod
    def from_gray(cls, value):
        return cls(value, value, value)

    @property
    def is_gray(self):
        return self.red == self.green == self.blue

    @property
    def gray(self):
        if not self.is_gray:
            msg = "The color is not gray."
            raise ValueError(msg)

        return self.red

    @gray.setter
    def gray(self, value):
        # TODO: Revisit alpha handling
        self.red = self.green = self.blue = value

    # / Gray

    # Name
    @classmethod
    def from_name(cls, value):
        hexcode = ...
        return cls.from_hexcode(hexcode)

    @property
    def is_named(self):
        return ...

    def name(self):
        if not self.is_named:
            msg = "The color is not named."
            raise ValueError(msg)

        return ...

    # / Name

    # Utils
    @property
    def luminance(self):
        # TODO: What about alpha?
        return 0.299 * self.red + 0.587 * self.green + 0.114 * self.blue

    @property
    def is_light(self):
        return self.luminance > 150

    @property
    def is_dark(self):
        return self.luminance <= 150
