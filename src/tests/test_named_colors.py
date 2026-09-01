import pytest
from faker import Faker
from matplotlib.colors import to_hex, to_rgb

from pier5.graphics.named_colors import (
    BaseColor,
    Css4Color,
    TableauColor,
    XkcdColor,
    clean_colors,
)

fake = Faker()


@pytest.mark.parametrize("prefix", ("tab", "xkcd"))
def test_clean_colors_key(prefix) -> None:
    key = "prefix:" + fake.color_name()
    value = fake.hex_color()

    expected_key = key.removeprefix(prefix).replace(" ", "_").upper()
    result_key = next(iter(clean_colors({key: value}).keys()))

    assert result_key == expected_key


def test_clean_colors_value_rgb() -> None:
    key = fake.color_name()
    value = fake.color_rgb_float()

    expected_value = to_hex(value).upper()
    result_value = next(iter(clean_colors({key: value}).values()))

    assert result_value == expected_value


def test_clean_colors_value_upper() -> None:
    key = fake.color_name()
    value = fake.hex_color().lower()

    expected_value = value.upper()
    result_value = next(iter(clean_colors({key: value}).values()))

    assert result_value == expected_value


def test_names_are_unique_within_enum() -> None:
    for enum_cls in (BaseColor, Css4Color, TableauColor, XkcdColor):
        names = [color.name for color in enum_cls]
        assert len(names) == len(set(names))


def test_names_are_sorted_alphabetically_except_base() -> None:
    for enum_cls in (Css4Color, TableauColor, XkcdColor):
        names = [color.name for color in enum_cls]
        assert names == sorted(names)


def test_names_are_upper_identifiers() -> None:
    for enum_cls in (BaseColor, Css4Color, TableauColor, XkcdColor):
        for color in enum_cls:
            assert color.name.isidentifier()
            assert color.name == color.name.upper()


def test_all_values_are_6_digit_hex() -> None:
    for enum_cls in (BaseColor, Css4Color, TableauColor, XkcdColor):
        for color in enum_cls:
            try:
                to_rgb(color)
            except ValueError:
                pytest.fail(f"{color} is not a valid color")
