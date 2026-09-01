import threading
from enum import Enum

from pier5 import BaseSketch
from pier5.graphics.named_colors import (
    BaseColor,
    Css4Color,
    TableauColor,
    XkcdColor,
)

__all__ = ("preview_named_colors",)


def hex_to_rgb(hex_code: str) -> tuple[int, int, int]:
    hex_code = hex_code.lstrip("#")
    return (
        int(hex_code[0:2], 16),
        int(hex_code[2:4], 16),
        int(hex_code[4:6], 16),
    )


def is_light(
    red: int | float,
    green: int | float,
    blue: int | float,
) -> bool:
    return 0.299 * red + 0.587 * green + 0.114 * blue > 150


class NamedColorPreviews(BaseSketch):
    WINDOW_WIDTH = 520
    WINDOW_HEIGHT = 600
    MIN_ROW_HEIGHT = 52.8
    TAB_HEIGHT = 40
    SEARCH_HEIGHT = 32
    SCROLLBAR_WIDTH = 12
    MIN_THUMB_HEIGHT = 24
    WHEEL_STEP = 24
    INFO_DURATION = 1.5
    INFO_PADDING = 8
    INFO_MARGIN = 12
    CARET_BLINK_MS = 530

    # Flat palette.
    BG = "#F5F6F8"
    PANEL = "#FFFFFF"
    PANEL_HOVER = "#ECF0F4"
    TAB_INACTIVE = "#E3E8EE"
    BORDER = "#DDE2E8"
    TEXT = "#2B2F36"
    TEXT_MUTED = "#8A929E"
    ACCENT = "#4C7DF0"

    def __init__(self) -> None:
        super().__init__()

        self.tabs = [
            ("Base", list(BaseColor)),
            ("CSS4", list(Css4Color)),
            ("Tableau", list(TableauColor)),
            ("XKCD", list(XkcdColor)),
        ]
        self.active_tab = 0
        self.scroll = 0.0
        self.dragging = False
        self.drag_offset = 0.0
        self.query = ""
        self.search_focused = False
        self.caret_visible = False
        self.caret_timer = None
        self.notice = ""
        self.notice_timer = None

    @property
    def colors(self) -> list[Enum]:
        return self.filter_colors(self.tabs[self.active_tab][1])

    def filter_colors(self, all_colors: list[Enum]) -> list[Enum]:
        query = self.query.strip().lower()
        if not query:
            return all_colors

        return [color for color in all_colors if query in color.name.lower() or query in color.value.lower()]

    @property
    def content_top(self) -> float:
        return float(self.TAB_HEIGHT + self.SEARCH_HEIGHT)

    @property
    def content_height(self) -> float:
        return float(self.height - self.content_top)

    @property
    def row_height(self) -> float:
        if not self.colors:
            return self.MIN_ROW_HEIGHT
        return max(self.MIN_ROW_HEIGHT, self.content_height / len(self.colors))

    @property
    def total_height(self) -> float:
        return float(self.row_height * len(self.colors))

    @property
    def max_scroll(self) -> float:
        return max(0.0, self.total_height - self.content_height)

    @property
    def thumb_height(self) -> float:
        if self.total_height <= self.content_height:
            return self.content_height
        return max(
            self.MIN_THUMB_HEIGHT,
            self.content_height * self.content_height / self.total_height,
        )

    @property
    def thumb_y(self) -> float:
        if self.max_scroll <= 0:
            return self.content_top
        track_height = self.content_height - self.thumb_height
        return self.content_top + track_height * (self.scroll / self.max_scroll)

    def set_scroll(self, value: float) -> None:
        self.scroll = max(0.0, min(value, self.max_scroll))

    def scroll_from_thumb_y(self, thumb_top: float) -> float:
        track_height = self.content_height - self.thumb_height
        if track_height <= 0:
            return 0.0
        return (thumb_top - self.content_top) / track_height * self.max_scroll

    def set_search_focus(self, focused: bool) -> None:
        self.search_focused = focused
        self.caret_visible = focused

        if focused:
            self._restart_caret_blink()
        elif self.caret_timer is not None:
            self.caret_timer.cancel()
            self.caret_timer = None

    def _restart_caret_blink(self) -> None:
        if self.caret_timer is not None:
            self.caret_timer.cancel()

        self.caret_timer = threading.Timer(self.CARET_BLINK_MS / 1000, self._toggle_caret)
        self.caret_timer.daemon = True
        self.caret_timer.start()

    def _toggle_caret(self) -> None:
        if not self.search_focused:
            return

        self.caret_visible = not self.caret_visible
        self.redraw()
        self._restart_caret_blink()

    def settings(self) -> None:
        self.size(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)

    def setup(self) -> None:
        self.window_title("Named Colors")
        self.text_size(14)
        self.text_align(self.CENTER, self.CENTER)
        self.is_looping = False

    def draw(self) -> None:
        self.background(self.BG)
        self.draw_tabs()
        self.draw_search()
        self.draw_rows()
        self.draw_scrollbar()
        self.draw_notice()

    def draw_tabs(self) -> None:
        tab_width = self.width / len(self.tabs)

        for index, (label, colors) in enumerate(self.tabs):
            active = index == self.active_tab

            self.fill(self.PANEL if active else self.TAB_INACTIVE)
            self.no_stroke()
            self.rect(index * tab_width, 0, tab_width, self.TAB_HEIGHT)

            if active:
                self.no_stroke()
                self.fill(self.ACCENT)
                self.rect(index * tab_width, self.TAB_HEIGHT - 2, tab_width, 2)

            self.fill(self.TEXT)
            text = f"{label} ({len(self.filter_colors(colors))})" if self.query else label
            self.text(text, index * tab_width + tab_width / 2, self.TAB_HEIGHT / 2)

    def draw_search(self) -> None:
        y = self.TAB_HEIGHT

        # Background band for the search row.
        self.fill(self.PANEL)
        self.no_stroke()
        self.rect(0, y, self.width, self.SEARCH_HEIGHT)

        # Inset input field.
        field_x = self.INFO_PADDING
        field_y = y + 6
        field_w = self.width - self.INFO_PADDING * 2
        field_h = self.SEARCH_HEIGHT - 12

        self.fill(self.BG)
        self.stroke(self.ACCENT if self.search_focused else self.BORDER)
        self.rect(field_x, field_y, field_w, field_h)

        self.no_stroke()
        self.text_align(self.LEFT, self.CENTER)
        if self.query:
            self.fill(self.TEXT)
            self.text(self.query, field_x + self.INFO_PADDING, field_y + field_h / 2)
        else:
            self.fill(self.TEXT_MUTED)
            self.text("Search...", field_x + self.INFO_PADDING, field_y + field_h / 2)

        if self.query:
            self.fill(self.TEXT_MUTED)
            self.text_align(self.CENTER, self.CENTER)
            self.text("×", field_x + field_w - self.INFO_PADDING, field_y + field_h / 2)

        if self.search_focused and self.caret_visible:
            caret_x = field_x + self.INFO_PADDING + (self.text_width(self.query) if self.query else 0)
            self.stroke(self.ACCENT)
            self.line(caret_x, field_y + 5, caret_x, field_y + field_h - 5)
            self.no_stroke()

        self.text_align(self.CENTER, self.CENTER)

    def draw_rows(self) -> None:
        # Clip to the content area below the tabs and search bar.
        self.clip(0, self.content_top, self.width, self.content_height)

        row_h = self.row_height
        for index, color in enumerate(self.colors):
            y = self.content_top + index * row_h - self.scroll
            if y + row_h <= self.content_top or y >= self.height:
                continue

            self.draw_row(color, y, row_h)

        self.no_clip()

    def draw_row(self, color: Enum, y: float, height: float) -> None:
        red, green, blue = hex_to_rgb(color.value)

        # Full-width row background in the color.
        self.fill(color.value)
        self.no_stroke()
        self.rect(0, y, self.width, height)

        # Contrasting text: name on the left, hex value on the right.
        self.fill(0 if is_light(red, green, blue) else 255)
        self.text_align(self.LEFT, self.CENTER)
        self.text(color.name, self.INFO_PADDING, y + height / 2)

        self.text_align(self.RIGHT, self.CENTER)
        self.text(color.value, self.width - self.SCROLLBAR_WIDTH - self.INFO_PADDING, y + height / 2)
        self.text_align(self.CENTER, self.CENTER)

    def draw_scrollbar(self) -> None:
        if self.max_scroll <= 0:
            return

        x = self.width - self.SCROLLBAR_WIDTH

        # Track.
        self.fill(self.PANEL_HOVER)
        self.no_stroke()
        self.rect(x + self.SCROLLBAR_WIDTH - 9, self.content_top, 9, self.content_height)

        # Thumb.
        self.fill(self.TEXT_MUTED)
        self.rect(x + self.SCROLLBAR_WIDTH - 9, self.thumb_y, 9, self.thumb_height)

    def draw_notice(self) -> None:
        if not self.notice:
            return

        box_width = self.text_width(self.notice) + 2 * self.INFO_PADDING
        box_height = self.text_ascent() + self.text_descent() + 2 * self.INFO_PADDING
        x = self.width - box_width - self.INFO_MARGIN
        y = self.height - box_height - self.INFO_MARGIN

        self.fill(31, 35, 41, 235)
        self.no_stroke()
        self.rect(x, y, box_width, box_height)

        self.fill(255)
        self.text_align(self.LEFT, self.CENTER)
        self.text(self.notice, x + self.INFO_PADDING, y + box_height / 2)
        self.text_align(self.CENTER, self.CENTER)

    def mouse_wheel(self, event) -> None:
        self.set_scroll(self.scroll + event.get_count() * self.WHEEL_STEP)
        self.redraw()

    def mouse_pressed(self) -> None:
        if self.mouse_y < self.TAB_HEIGHT:
            self.select_tab()
            return

        if self.mouse_y < self.content_top:
            clear_x = self.width - self.INFO_PADDING - self.SEARCH_HEIGHT
            if self.query and self.mouse_x >= clear_x:
                self.query = ""
                self.scroll = 0.0
            self.set_search_focus(True)
            self.redraw()
            return

        self.set_search_focus(False)

        if self.mouse_x >= self.width - self.SCROLLBAR_WIDTH:
            self.handle_scrollbar_press()
            return

        self.select_color_under_mouse()

    def key_pressed(self) -> None:
        if not self.search_focused:
            return

        if self.key in (self.BACKSPACE, self.DELETE):
            self.query = self.query[:-1]
        elif len(self.key) == 1 and self.key.isprintable():
            self.query += self.key

        self.caret_visible = True
        self._restart_caret_blink()

        self.scroll = 0.0
        self.redraw()

    def mouse_dragged(self) -> None:
        if not self.dragging:
            return

        thumb_top = self.mouse_y - self.drag_offset
        self.set_scroll(self.scroll_from_thumb_y(thumb_top))
        self.redraw()

    def mouse_released(self) -> None:
        self.dragging = False

    def select_tab(self) -> None:
        index = int(self.mouse_x // (self.width / len(self.tabs)))
        if 0 <= index < len(self.tabs):
            self.set_search_focus(False)
            self.active_tab = index
            self.scroll = 0.0
            self.dragging = False
            self.redraw()

    def handle_scrollbar_press(self) -> None:
        if self.mouse_y < self.thumb_y:
            self.set_scroll(self.scroll - self.content_height)
        elif self.mouse_y > self.thumb_y + self.thumb_height:
            self.set_scroll(self.scroll + self.content_height)
        else:
            self.dragging = True
            self.drag_offset = self.mouse_y - self.thumb_y

        self.redraw()

    def select_color_under_mouse(self) -> None:
        index = int((self.mouse_y - self.content_top + self.scroll) // self.row_height)
        if 0 <= index < len(self.colors):
            self.show_notice(self.colors[index])

    def show_notice(self, color: Enum) -> None:
        print(f"{type(color).__name__}.{color.name} {color.value}")  # noqa: T201

        self.notice = f"{type(color).__name__}.{color.name}  {color.value} → Printed to the console."

        self.redraw()

        if self.notice_timer is not None:
            self.notice_timer.cancel()
        self.notice_timer = threading.Timer(self.INFO_DURATION, self.hide_notice)
        self.notice_timer.daemon = True
        self.notice_timer.start()

    def hide_notice(self) -> None:
        self.notice = ""
        self.redraw()


def preview_named_colors() -> None:
    """
    Open an interactive, tabbed preview of every named color enum.
    """
    NamedColorPreviews().run_sketch()


if __name__ == "__main__":
    preview_named_colors()
