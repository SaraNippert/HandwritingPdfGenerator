# font identifiers (stable keys like "noto_sans_jp")
# optional metadata (display label, ReportLab internal name, file name)
# one exported constant collection used everywhere as source of truth

# The first font in each dictionary will be the default font for the corresponding alphabet.

from dataclasses import dataclass


@dataclass(frozen=True)
class FontDefinition:
    id: str  # key
    display_name: str  # user-facing label
    font_directory: str
    file_name: str

# all available fonts for the Japanese alphabets
JAPANESE_FONTS: dict[str, FontDefinition] = {
    "noto_sans_jp": FontDefinition(
        id="noto_sans_jp",
        display_name="Noto Sans JP",
        font_directory="Noto_Sans_JP",
        file_name="NotoSansJP-VariableFont_wght.ttf",
    )
}
# list of font ids for use by presets
JAPANESE_FONT_LIST: list[str] = list(JAPANESE_FONTS.keys())

# all available fonts for the latin alphabet
LATIN_FONTS: dict[str, FontDefinition] = {
    "playwrite_be_wal_guides" : FontDefinition(
        id="playwrite_be_wal_guides",
        display_name="Playwright BE WAL Guides",
        font_directory="Playwrighte_BE_WAL_Guides",
        file_name="PlaywriteBEWALGuides-Regular.ttf",
    ),
    "playfair_display": FontDefinition(
        id="playfair_display",
        display_name="PlayfairDisplay",
        font_directory="Playfair_Display",
        file_name="PlayfairDisplay-VariableFont_wght.ttf",
    )
}
LATIN_FONT_LIST: list[str] = list(LATIN_FONTS.keys())

ALL_FONTS: dict[str, FontDefinition] = {
    **JAPANESE_FONTS,
    **LATIN_FONTS
}