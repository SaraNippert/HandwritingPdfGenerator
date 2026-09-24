# grid/box placement logic

from dataclasses import dataclass
from reportlab.lib.pagesizes import LETTER, landscape, portrait
from enum import Enum

class PageOrientation(str, Enum):
    PORTRAIT = "portrait"
    LANDSCAPE = "landscape"

@dataclass(frozen=True)
class PageLayout:
    """
    Immutable coordinate definition for drawing a worksheet page.

    Each attribute stores an absolute position (in PDF canvas units/points)
    used by rendering code to place major visual elements on the page.
    """

    # Use defaults provided by reportlab
    # default to landscape
    page_orientation: PageOrientation = PageOrientation.LANDSCAPE
    # should always be portrait sizing
    base_page_size: tuple[float, float] = LETTER

    # set margins (.5in default)
    margin_left: float = 36.0
    margin_right: float = 36.0
    margin_top: float = 36.0
    margin_bottom: float = 36.0

    # default font sizes & spacing
    title_top_offset: float = 12.0
    title_font_size: int = 12
    text_font_size: int = 12
    line_gap: int = 10

    # colors (set to light gray to be easy to trace over)
    text_fill_color: str = "#c0c1c0"
    guide_border_color: str = "#c0c1c0"
    guide_center_color: str = "#c0c1c0"

    # Guide cell geometry policy
    guide_cell_width_ratio: float = 1.5
    guide_cell_height_ratio: float = 1.5
    guide_cell_gap_ratio: float = 0.25
    guide_baseline_offset_ratio: float = 0.25

    # Guideline style policy
    guide_line_width: float = 0.1
    guide_dash_on: float = 0.5
    guide_dash_off: float = 1.0

    @property
    def page_size(self) -> tuple[float, float]:
        if self.page_orientation is PageOrientation.LANDSCAPE:
            return landscape(self.base_page_size)
        else:
            return portrait(self.base_page_size)

    @property
    def page_width(self) -> float:
        return self.page_size[0]

    @property
    def page_height(self) -> float:
        return self.page_size[1]

    @property
    def left(self) -> float:
        return self.margin_left

    @property
    def right(self) -> float:
        return self.page_width - self.margin_right

    @property
    def top(self) -> float:
        return self.page_height - self.margin_top

    @property
    def bottom(self) -> float:
        return self.margin_bottom

    # Optional convenience metrics for renderer
    @property
    def line_height(self) -> float:
        return self.text_font_size + self.line_gap

    @property
    def first_row_baseline(self) -> float:
        return (self.top - self.title_top_offset) - self.line_height

    # Derived guide geometry
    @property
    def guide_cell_width(self) -> float:
        return self.text_font_size * self.guide_cell_width_ratio

    @property
    def guide_cell_height(self) -> float:
        return self.text_font_size * self.guide_cell_height_ratio

    @property
    def guide_cell_gap(self) -> float:
        return self.text_font_size * self.guide_cell_gap_ratio

    @property
    def guide_cell_step(self) -> float:
        return self.guide_cell_width + self.guide_cell_gap

    @property
    def guide_baseline_offset(self) -> float:
        return self.guide_cell_height * self.guide_baseline_offset_ratio


def build_single_page_layout(page_orientation: PageOrientation) -> PageLayout:
    """
    Build and return the default one-page layout configuration.

    Returns:
        PageLayout: A frozen layout object containing the canonical
        coordinates used by renderer/generator components.
    """
    return PageLayout(page_orientation=page_orientation)
