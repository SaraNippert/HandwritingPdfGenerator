from enum import Enum

import typer
import questionary

from ..domain.worksheet_preset import WorksheetPreset, RowRenderMode, OutputLayoutMode
from ..pdf.layout import PageOrientation, FontSize
from ..presets.french import FRENCH_PRESETS
from ..presets.katakana import KATAKANA_PRESETS
from ..presets.hiragana import HIRAGANA_PRESETS

ALL_PRESETS: dict[str, WorksheetPreset] = {
    **KATAKANA_PRESETS,
    **HIRAGANA_PRESETS,
    **FRENCH_PRESETS
}

def select_worksheet_preset() -> ALL_PRESETS:
    """Prompt the user to select a PDF type and return it as an enum value.

       Returns:
           PdfOptions: The selected PDF type (`katakana` or `hiragana`).

       Raises:
           typer.Abort: If the prompt is cancelled (for example with Ctrl+C or Esc).
       """

    choice = questionary.select(
        "Select PDF type:",
        choices=[option for option in ALL_PRESETS],
    ).ask()

    if choice is None:
        raise typer.Abort()  # handles Ctrl+C / escape cleanly

    # print(choice)
    return ALL_PRESETS[choice]

def select_row_render_mode() -> RowRenderMode:
    choice = questionary.select(
        "Select row type:",
        choices=[option for option in RowRenderMode]
    ).ask()
    if choice is None:
        choice = RowRenderMode.REPEAT # default to repeat

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