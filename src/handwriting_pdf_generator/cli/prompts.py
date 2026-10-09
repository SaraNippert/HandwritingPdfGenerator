from enum import Enum

import typer
import questionary

from ..domain.worksheet_preset import WorksheetPreset, RowRenderMode, OutputLayoutMode
from ..pdf.layout import PageOrientation, FontSize

from ..presets.french import FRENCH_PRESETS
from ..presets.katakana import KATAKANA_PRESETS
from ..presets.hiragana import HIRAGANA_PRESETS
from ..presets.kana import KANA_PRESETS
from ..presets.kanji import KANJI_PRESETS

PRESET_GROUPS: dict[str, dict[str, WorksheetPreset]] = {
    "Katakana": KATAKANA_PRESETS,
    "Hiragana": HIRAGANA_PRESETS,
    "Kana": KANA_PRESETS,
    "Kanji": KANJI_PRESETS,
    "French": FRENCH_PRESETS,
}


def select_worksheet_preset() -> WorksheetPreset:
    """Prompt the user to select a PDF type and return it as an enum value.

       Returns:
           PdfOptions: The selected PDF type (`katakana` or `hiragana`).

       Raises:
           typer.Abort: If the prompt is cancelled (for example with Ctrl+C or Esc).
       """

    group_choice = questionary.select(
        "Select character set:",
        choices=list(PRESET_GROUPS.keys()),
    ).ask()

    if group_choice is None:
        raise typer.Abort()

    presets_in_group = PRESET_GROUPS[group_choice]

    preset_choices = {
        preset.display_name: preset
        for preset in presets_in_group.values()
    }

    preset_choice = questionary.select(
        f"Select {group_choice.lower()} worksheet:",
        choices=list(preset_choices.keys()),
    ).ask()

    if preset_choice is None:
        raise typer.Abort()

    return preset_choices[preset_choice]


def select_row_render_mode() -> RowRenderMode:
    choice = questionary.select(
        "Select row type:",
        choices=[option for option in RowRenderMode]
    ).ask()
    if choice is None:
        choice = RowRenderMode.REPEAT  # default to repeat

    return RowRenderMode(choice)


def select_font_size() -> FontSize:
    # do not allow user to input their own font size, only allow tested font sizes
    choice = questionary.select(
        "Select font size:",
        choices=[option.name for option in FontSize],
    ).ask()

    if choice is None:
        choice = FontSize.FOURTEEN.name

    return FontSize[choice]


def select_page_orientation() -> PageOrientation:
    choice = questionary.select(
        "Select page orientation:",
        choices=[option.value for option in PageOrientation]
    ).ask()
    return PageOrientation(choice)


def select_output_mode() -> OutputLayoutMode:
    choice = questionary.select(
        "Select output mode:",
        choices=[option.value for option in OutputLayoutMode]
    ).ask()
    return OutputLayoutMode(choice)


def header() -> None:
    """Print a styled banner shown at CLI startup."""
    typer.secho("╭──────────────────────────────────────╮", fg=typer.colors.GREEN, bold=True)
    typer.secho("│    Handwriting PDF Generator CLI     │", fg=typer.colors.GREEN, bold=True)
    typer.secho("╰──────────────────────────────────────╯", fg=typer.colors.GREEN, bold=True)


def booklet_instructions() -> None:
    typer.secho("To print the booklet, print two pages per sheet, double-sided.", fg=typer.colors.GREEN, bold=True)
