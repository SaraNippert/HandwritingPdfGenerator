import pytest

from handwriting_pdf_generator.domain.font_catalog import (
    ALL_FONTS,
    JAPANESE_FONT_LIST,
    JAPANESE_FONTS,
    LATIN_FONT_LIST,
    LATIN_FONTS,
)
from handwriting_pdf_generator.domain.worksheet_preset import (
    GuideStyle,
    RowRenderMode,
    WorksheetPreset,
)


def test_worksheet_preset_is_hashable_and_uses_enum_values():
    preset = WorksheetPreset(
        id="sample",
        display_name="Sample",
        prompts=("a", "b"),
        available_fonts=("font-1",),
        guide_style=GuideStyle.PLUS_DOTTED,
    )

    assert preset == WorksheetPreset(
        id="sample",
        display_name="Sample",
        prompts=("a", "b"),
        available_fonts=("font-1",),
        guide_style=GuideStyle.PLUS_DOTTED,
    )
    assert hash(preset) == hash(WorksheetPreset("sample", "Sample", ("a", "b"), ("font-1",), GuideStyle.PLUS_DOTTED))
    assert RowRenderMode.REPEAT == "repeat"
    assert GuideStyle.NONE == "none"


@pytest.mark.parametrize(
    "catalog,font_list",
    [
        (JAPANESE_FONTS, JAPANESE_FONT_LIST),
        (LATIN_FONTS, LATIN_FONT_LIST),
    ],
)
def test_font_catalog_lists_match_dictionary_keys(catalog, font_list):
    assert list(catalog) == font_list
    assert list(ALL_FONTS)[0] in ALL_FONTS
    for font_id, definition in catalog.items():
        assert definition.id == font_id
        assert definition.display_name
        assert definition.font_directory
        assert definition.file_name.endswith(".ttf")
