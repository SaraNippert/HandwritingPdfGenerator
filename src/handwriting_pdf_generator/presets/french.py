from ..domain.worksheet_preset import WorksheetPreset, GuideStyle
from ..domain.font_catalog import LATIN_FONT_LIST

LOWERCASE: tuple[str, ...] = (
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
    'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
    'u', 'v', 'w', 'x', 'y', 'z'
)

UPPERCASE: tuple[str, ...] = (
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
    'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X', 'Y', 'Z'
)

FRENCH_PRESETS: dict[str, WorksheetPreset] = {
    "french_lowercase": WorksheetPreset(
        id="french_lowercase",
        display_name="French Lowercase",
        prompts=LOWERCASE,
        available_fonts=LATIN_FONT_LIST,
        guide_style=GuideStyle.NONE
    )
}
