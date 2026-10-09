from handwriting_pdf_generator.domain.worksheet_preset import GuideStyle
from handwriting_pdf_generator.presets.french import FRENCH_PRESETS, LOWERCASE
from handwriting_pdf_generator.presets.hiragana import (
    HIRAGANA_GOJUON,
    HIRAGANA_PRESETS,
)
from handwriting_pdf_generator.presets.katakana import (
    KATAKANA_GOJUON,
    KATAKANA_PRESETS,
)


def test_hiragana_and_katakana_presets_cover_expected_sequences():
    assert len(HIRAGANA_GOJUON) == 46
    assert len(KATAKANA_GOJUON) == 46
    assert HIRAGANA_PRESETS["hiragana_gojuon"].prompts == HIRAGANA_GOJUON
    assert KATAKANA_PRESETS["katakana_gojuon"].prompts == KATAKANA_GOJUON


def test_french_and_japanese_presets_wire_fonts_and_guides():
    assert FRENCH_PRESETS["french_lowercase"].prompts == LOWERCASE
    assert FRENCH_PRESETS["french_lowercase"].guide_style is GuideStyle.NONE
    assert HIRAGANA_PRESETS["hiragana_gojuon"].available_fonts == HIRAGANA_PRESETS["hiragana_dakuten_handakuten"].available_fonts
    assert KATAKANA_PRESETS["katakana_gojuon"].available_fonts == KATAKANA_PRESETS["katakana_dakuten_handakuten"].available_fonts
