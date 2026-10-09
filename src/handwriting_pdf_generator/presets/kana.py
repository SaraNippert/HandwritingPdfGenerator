# this file combines katakana and hiragana presets

from .hiragana import HIRAGANA_GOJUON, HIRAGANA_DAKUTEN_HANDAKUTEN
from .katakana import KATAKANA_GOJUON, KATAKANA_DAKUTEN_HANDAKUTEN
from ..domain.worksheet_preset import WorksheetPreset, GuideStyle
from ..domain.font_catalog import JAPANESE_FONT_LIST

KANA_PRESETS: dict[str, WorksheetPreset] = {
    "kana_grid": WorksheetPreset(
        id="kana_grid",
        display_name="Kana Grid",
        prompts=KATAKANA_GOJUON + HIRAGANA_GOJUON,
        available_fonts=JAPANESE_FONT_LIST,
        guide_style=GuideStyle.PLUS_DOTTED,
    ),
    "kana_grid_expanded": WorksheetPreset(
        id="kana_grid",
        display_name="Kana Grid",
        prompts=KATAKANA_GOJUON + KATAKANA_DAKUTEN_HANDAKUTEN + HIRAGANA_GOJUON + HIRAGANA_DAKUTEN_HANDAKUTEN,
        available_fonts=JAPANESE_FONT_LIST,
        guide_style=GuideStyle.PLUS_DOTTED,
    )
}
