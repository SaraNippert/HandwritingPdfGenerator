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
        prompts: Ordered tuple of characters/phrases/sentences included in the worksheet.
            A tuple is used to keep the preset immutable and hashable.
        available_fonts: fonts which can be used with this preset
            (not all fonts work for all languages)
        guide_style: the lines around the character to be used to help the
            user visualize character placement
    """
    id: str
    display_name: str
    prompts: tuple[str, ...]  # Sequence of characters to generate practice rows from.
    available_fonts: tuple[str, ...] #
    guide_style: GuideStyle = GuideStyle.NONE
