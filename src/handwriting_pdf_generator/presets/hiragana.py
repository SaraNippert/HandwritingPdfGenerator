# This file defines constants related to Hiragana
from ..domain.worksheet_preset import WorksheetPreset, GuideStyle
from ..domain.font_catalog import JAPANESE_FONT_LIST

# Base (gojuon) hiragana set in common row order.
HIRAGANA_GOJUON: tuple[str, ...] = (
    "あ", "い", "う", "え", "お",
    "か", "き", "く", "け", "こ",
    "さ", "し", "す", "せ", "そ",
    "た", "ち", "つ", "て", "と",
    "な", "に", "ぬ", "ね", "の",
    "は", "ひ", "ふ", "へ", "ほ",
    "ま", "み", "む", "め", "も",
    "や", "ゆ", "よ",
    "ら", "り", "る", "れ", "ろ",
    "わ", "を", "ん",
)

# Voiced + semi-voiced variants often practiced separately.
HIRAGANA_DAKUTEN_HANDAKUTEN: tuple[str, ...] = (
    "が", "ぎ", "ぐ", "げ", "ご",
    "ざ", "じ", "ず", "ぜ", "ぞ",
    "だ", "ぢ", "づ", "で", "ど",
    "ば", "び", "ぶ", "べ", "ぼ",
    "ぱ", "ぴ", "ぷ", "ぺ", "ぽ",
)

HIRAGANA_PRESETS: dict[str, WorksheetPreset] = {
    "hiragana_grid": WorksheetPreset(
        id="hiragana_grid",
        display_name="Hiragana Grid",
        characters=HIRAGANA_GOJUON,
        available_fonts=JAPANESE_FONT_LIST,
        guide_style=GuideStyle.PLUS_DOTTED
    ),
    "hiragana_grid_expanded": WorksheetPreset(
        id="hiragana_grid_expanded",
        display_name="Hiragana Grid Expanded",
        characters=HIRAGANA_GOJUON + HIRAGANA_DAKUTEN_HANDAKUTEN,
        available_fonts=JAPANESE_FONT_LIST,
        guide_style=GuideStyle.PLUS_DOTTED
    )
}
