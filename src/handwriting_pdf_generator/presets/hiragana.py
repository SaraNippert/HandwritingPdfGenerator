# This file defines constants related to Hiragana
from ..domain.worksheet_preset import WorksheetPreset, GuideStyle, PromptEntry
from ..domain.font_catalog import JAPANESE_FONT_LIST

# Base (gojuon) hiragana set in common row order.
HIRAGANA_GOJUON: tuple[PromptEntry, ...] = (
    PromptEntry("あ", "a"),
    PromptEntry("い", "i"),
    PromptEntry("う", "u"),
    PromptEntry("え", "e"),
    PromptEntry("お", "o"),
    PromptEntry("か", "ka"),
    PromptEntry("き", "ki"),
    PromptEntry("く", "ku"),
    PromptEntry("け", "ke"),
    PromptEntry("こ", "ko"),
    PromptEntry("さ", "sa"),
    PromptEntry("し", "shi"),
    PromptEntry("す", "su"),
    PromptEntry("せ", "se"),
    PromptEntry("そ", "so"),
    PromptEntry("た", "ta"),
    PromptEntry("ち", "chi"),
    PromptEntry("つ", "tsu"),
    PromptEntry("て", "te"),
    PromptEntry("と", "to"),
    PromptEntry("な", "na"),
    PromptEntry("に", "ni"),
    PromptEntry("ぬ", "nu"),
    PromptEntry("ね", "ne"),
    PromptEntry("の", "no"),
    PromptEntry("は", "ha"),
    PromptEntry("ひ", "hi"),
    PromptEntry("ふ", "fu"),
    PromptEntry("へ", "he"),
    PromptEntry("ほ", "ho"),
    PromptEntry("ま", "ma"),
    PromptEntry("み", "mi"),
    PromptEntry("む", "mu"),
    PromptEntry("め", "me"),
    PromptEntry("も", "mo"),
    PromptEntry("や", "ya"),
    PromptEntry("ゆ", "yu"),
    PromptEntry("よ", "yo"),
    PromptEntry("ら", "ra"),
    PromptEntry("り", "ri"),
    PromptEntry("る", "ru"),
    PromptEntry("れ", "re"),
    PromptEntry("ろ", "ro"),
    PromptEntry("わ", "wa"),
    PromptEntry("を", "wo"),
    PromptEntry("ん", "n"),
)

# Voiced + semi-voiced variants often practiced separately.
HIRAGANA_DAKUTEN_HANDAKUTEN: tuple[PromptEntry, ...] = (
    PromptEntry("が", "ga"),
    PromptEntry("ぎ", "gi"),
    PromptEntry("ぐ", "gu"),
    PromptEntry("げ", "ge"),
    PromptEntry("ご", "go"),
    PromptEntry("ざ", "za"),
    PromptEntry("じ", "ji"),
    PromptEntry("ず", "zu"),
    PromptEntry("ぜ", "ze"),
    PromptEntry("ぞ", "zo"),
    PromptEntry("だ", "da"),
    PromptEntry("ぢ", "ji"),
    PromptEntry("づ", "zu"),
    PromptEntry("で", "de"),
    PromptEntry("ど", "do"),
    PromptEntry("ば", "ba"),
    PromptEntry("び", "bi"),
    PromptEntry("ぶ", "bu"),
    PromptEntry("べ", "be"),
    PromptEntry("ぼ", "bo"),
    PromptEntry("ぱ", "pa"),
    PromptEntry("ぴ", "pi"),
    PromptEntry("ぷ", "pu"),
    PromptEntry("ぺ", "pe"),
    PromptEntry("ぽ", "po"),
)

HIRAGANA_PRESETS: dict[str, WorksheetPreset] = {
    "hiragana_gojuon": WorksheetPreset(
        id="hiragana_gojuon",
        display_name="Hiragana Gojuon",
        prompts=HIRAGANA_GOJUON,
        available_fonts=JAPANESE_FONT_LIST,
        guide_style=GuideStyle.PLUS_DOTTED
    ),
    "hiragana_dakuten_handakuten": WorksheetPreset(
        id="hiragana_dakuten_handakuten",
        display_name="Hiragana Dakuten Handakuten",
        prompts=HIRAGANA_DAKUTEN_HANDAKUTEN,
        available_fonts=JAPANESE_FONT_LIST,
        guide_style=GuideStyle.PLUS_DOTTED
    )
}
