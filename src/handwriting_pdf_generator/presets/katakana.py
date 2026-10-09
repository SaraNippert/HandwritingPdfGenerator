# This file defines contestants related to Katakana
from ..domain.worksheet_preset import WorksheetPreset, GuideStyle
from ..domain.font_catalog import JAPANESE_FONT_LIST

# Base (gojuon) katakana set in common row order.
KATAKANA_GOJUON: tuple[str, ...] = (
    "ア", "イ", "ウ", "エ", "オ",
    "カ", "キ", "ク", "ケ", "コ",
    "サ", "シ", "ス", "セ", "ソ",
    "タ", "チ", "ツ", "テ", "ト",
    "ナ", "ニ", "ヌ", "ネ", "ノ",
    "ハ", "ヒ", "フ", "ヘ", "ホ",
    "マ", "ミ", "ム", "メ", "モ",
    "ヤ", "ユ", "ヨ",
    "ラ", "リ", "ル", "レ", "ロ",
    "ワ", "ヲ", "ン",
)

# Voiced + semi-voiced variants often practiced separately.
KATAKANA_DAKUTEN_HANDAKUTEN: tuple[str, ...] = (
    "ガ", "ギ", "グ", "ゲ", "ゴ",
    "ザ", "ジ", "ズ", "ゼ", "ゾ",
    "ダ", "ヂ", "ヅ", "デ", "ド",
    "バ", "ビ", "ブ", "ベ", "ボ",
    "パ", "ピ", "プ", "ペ", "ポ",
)

KATAKANA_PRESETS: dict[str, WorksheetPreset] = {
    "katakana_gojuon": WorksheetPreset(
        id="katakana_gojuon",
        display_name="Katakana Gojuon",
        prompts=KATAKANA_GOJUON,
        available_fonts=JAPANESE_FONT_LIST,
        guide_style=GuideStyle.PLUS_DOTTED
    ),
    "katakana_dakuten_handakuten": WorksheetPreset(
        id="katakana_dakuten_handakuten",
        display_name="Katakana Dakuten Handakuten",
        prompts=KATAKANA_DAKUTEN_HANDAKUTEN,
        available_fonts=JAPANESE_FONT_LIST,
        guide_style=GuideStyle.PLUS_DOTTED
    )
}
