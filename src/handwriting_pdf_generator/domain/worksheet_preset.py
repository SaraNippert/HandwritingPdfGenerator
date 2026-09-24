from dataclasses import dataclass
from enum import StrEnum

class RowRenderMode(StrEnum):
    REPEAT = "repeat"
    SINGLE = "single"

class GuideStyle(StrEnum):
    NONE = "none"
    PLUS_DOTTED = "plus_dotted"

@dataclass(frozen=True)
class WorksheetPreset:
    """
    Immutable reusable worksheet configuration.

    Attributes:
        id: Stable internal identifier for the preset (e.g., "katakana_base").
        display_name: Human-readable name shown in UI/CLI output
            (e.g., "Katakana (Base Gojuon)").
        characters: Ordered tuple of characters included in the worksheet.
            A tuple is used to keep the preset immutable and hashable.
    """

    id: str  # Stable machine-friendly preset key.
    display_name: str  # User-facing preset label.
    characters: tuple[str, ...]  # Sequence of characters to generate practice rows from.
    available_fonts: tuple[str, ...] # fonts which can be used with this preset (not all fonts work for all languages)
    guide_style: GuideStyle = GuideStyle.NONE
