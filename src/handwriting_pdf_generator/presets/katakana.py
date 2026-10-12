# This file defines contestants related to Katakana
from ..domain.worksheet_preset import WorksheetPreset, GuideStyle, PromptEntry
from ..domain.font_catalog import JAPANESE_FONT_LIST

# Base (gojuon) katakana set in common row order.
KATAKANA_GOJUON: tuple[PromptEntry, ...] = (
    PromptEntry("ア", "a"),
    PromptEntry("イ", "i"),
    PromptEntry("ウ", "u"),
    PromptEntry("エ", "e"),
    PromptEntry("オ", "o"),
    PromptEntry("カ", "ka"),
    PromptEntry("キ", "ki"),
    PromptEntry("ク", "ku"),
    PromptEntry("ケ", "ke"),
    PromptEntry("コ", "ko"),
    PromptEntry("サ", "sa"),
    PromptEntry("シ", "shi"),
    PromptEntry("ス", "su"),
    PromptEntry("セ", "se"),
    PromptEntry("ソ", "so"),
    PromptEntry("タ", "ta"),
    PromptEntry("チ", "chi"),
    PromptEntry("ツ", "tsu"),
    PromptEntry("テ", "te"),
    PromptEntry("ト", "to"),
    PromptEntry("ナ", "na"),
    PromptEntry("ニ", "ni"),
    PromptEntry("ヌ", "nu"),
    PromptEntry("ネ", "ne"),
    PromptEntry("ノ", "no"),
    PromptEntry("ハ", "ha"),
    PromptEntry("ヒ", "hi"),
    PromptEntry("フ", "fu"),
    PromptEntry("ヘ", "he"),
    PromptEntry("ホ", "ho"),
    PromptEntry("マ", "ma"),
    PromptEntry("ミ", "mi"),
    PromptEntry("ム", "mu"),
    PromptEntry("メ", "me"),
    PromptEntry("モ", "mo"),
    PromptEntry("ヤ", "ya"),
    PromptEntry("ユ", "yu"),
    PromptEntry("ヨ", "yo"),
    PromptEntry("ラ", "ra"),
    PromptEntry("リ", "ri"),
    PromptEntry("ル", "ru"),
    PromptEntry("レ", "re"),
    PromptEntry("ロ", "ro"),
    PromptEntry("ワ", "wa"),
    PromptEntry("ヲ", "wo"),
    PromptEntry("ン", "n"),
)

# Voiced + semi-voiced variants often practiced separately.
KATAKANA_DAKUTEN_HANDAKUTEN: tuple[PromptEntry, ...] = (
    PromptEntry("ガ", "ga"),
    PromptEntry("ギ", "gi"),
    PromptEntry("グ", "gu"),
    PromptEntry("ゲ", "ge"),
    PromptEntry("ゴ", "go"),
    PromptEntry("ザ", "za"),
    PromptEntry("ジ", "ji"),
    PromptEntry("ズ", "zu"),
    PromptEntry("ゼ", "ze"),
    PromptEntry("ゾ", "zo"),
    PromptEntry("ダ", "da"),
    PromptEntry("ヂ", "ji"),
    PromptEntry("ヅ", "zu"),
    PromptEntry("デ", "de"),
    PromptEntry("ド", "do"),
    PromptEntry("バ", "ba"),
    PromptEntry("ビ", "bi"),
    PromptEntry("ブ", "bu"),
    PromptEntry("ベ", "be"),
    PromptEntry("ボ", "bo"),
    PromptEntry("パ", "pa"),
    PromptEntry("ピ", "pi"),
    PromptEntry("プ", "pu"),
    PromptEntry("ペ", "pe"),
    PromptEntry("ポ", "po"),
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
