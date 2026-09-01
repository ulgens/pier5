from enum import Enum

from matplotlib.colors import (
    BASE_COLORS,
    CSS4_COLORS,
    TABLEAU_COLORS,
    XKCD_COLORS,
    to_hex,
)

__all__ = (
    "BaseColor",
    "Css4Color",
    "TableauColor",
    "XkcdColor",
)


def clean_colors(colors: dict) -> dict[str, str]:
    """
    Converts `"xkcd:light pastel green": "#b2fba5"` to `"LIGHT_PASTEL_GREEN": "#B2FBA5"`.
    Keys are cleaned for enum conversion; values are normalized to uppercase hex for cosmetic purposes.
    """

    clean_colors = {}

    for key, value in colors.items():
        # Key - Remove prefixes
        new_key = key.removeprefix("xkcd:")
        new_key = new_key.removeprefix("tab:")

        # Key - Replace invalid chars for an identifier
        new_key = new_key.replace(" ", "_")
        new_key = new_key.replace("/", "_")
        new_key = new_key.replace("'", "")

        # Key - Upper
        new_key = new_key.upper()

        # Value - Upper & RGB to HEX
        new_value = value.upper() if isinstance(value, str) else to_hex(value).upper()

        clean_colors[new_key] = new_value

    return clean_colors


BaseColor = Enum(
    "BaseColor",
    clean_colors(BASE_COLORS),
    type=str,
)

Css4Color = Enum(
    "Css4Color",
    clean_colors(CSS4_COLORS),
    type=str,
)

TableauColor = Enum(
    "TableauColor",
    clean_colors(TABLEAU_COLORS),
    type=str,
)

XkcdColor = Enum(
    "XkcdColor",
    clean_colors(XKCD_COLORS),
    type=str,
)
