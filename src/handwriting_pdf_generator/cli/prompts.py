from enum import StrEnum

import typer
import questionary

from ..domain.worksheet_preset import (
    WorksheetPreset,
    WorksheetSection,
    RowRenderMode,
    OutputLayoutMode, PromptEntry
)
from ..pdf.layout import PageOrientation, FontSize

from ..presets.french import FRENCH_PRESETS
from ..presets.katakana import KATAKANA_PRESETS
from ..presets.hiragana import HIRAGANA_PRESETS
from ..presets.kanji import KANJI_PRESETS


class PresetSelectionMode(StrEnum):
    SINGLE = "single"
    COMBINE = "combine"


LANGUAGE_PRESET_GROUPS: dict[str, dict[str, WorksheetPreset]] = {
    "Japanese": {
        **KATAKANA_PRESETS,
        **HIRAGANA_PRESETS,
        **KANJI_PRESETS,
    },
    "French": {
        **FRENCH_PRESETS,
    },
}

LANGUAGE_CATEGORIES: dict[str, dict[str, dict[str, WorksheetPreset]]] = {
    "Japanese": {
        "Katakana": KATAKANA_PRESETS,
        "Hiragana": HIRAGANA_PRESETS,
        "Kanji": KANJI_PRESETS,
    },
    "French": {
        "French": FRENCH_PRESETS,
    },
}


def select_worksheet_preset() -> WorksheetPreset:
    """Prompt the user to select a PDF type and return it as an enum value.

       Returns:
           PdfOptions: The selected PDF type (`katakana` or `hiragana`).

       Raises:
           typer.Abort: If the prompt is cancelled (for example with Ctrl+C or Esc).
       """

    selection_mode = select_preset_selection_mode()
    language_name = select_language()

    if selection_mode is PresetSelectionMode.SINGLE:
        category_name = select_category(language_name)
        return select_single_preset_from_category(language_name, category_name)

    selected_presets = select_multiple_presets_for_language(language_name)
    return build_combined_preset(language_name, selected_presets)


def select_preset_selection_mode() -> PresetSelectionMode:
    choice = questionary.select(
        "How would you like to build the worksheet?",
        choices=[
            "Single preset",
            "Combine multiple presets",
        ],
    ).ask()

    if choice is None:
        raise typer.Abort()

    if choice == "Single preset":
        return PresetSelectionMode.SINGLE

    return PresetSelectionMode.COMBINE


def select_language() -> str:
    choice = questionary.select(
        "Select language:",
        choices=list(LANGUAGE_CATEGORIES.keys()),
    ).ask()

    if choice is None:
        raise typer.Abort()

    return choice


def select_category(language_name: str) -> str:
    categories = LANGUAGE_CATEGORIES[language_name]

    if not categories:
        typer.secho(f"No categories available for {language_name}.", fg=typer.colors.RED)
        raise typer.Abort()

    choice = questionary.select(
        f"Select {language_name.lower()} character set:",
        choices=list(categories.keys()),
    ).ask()

    if choice is None:
        raise typer.Abort()

    return choice


def select_single_preset_from_category(language_name: str, category_name: str) -> WorksheetPreset:
    presets_in_category = LANGUAGE_CATEGORIES[language_name][category_name]

    if not presets_in_category:
        typer.secho(
            f"No presets available for {language_name} / {category_name}.",
            fg=typer.colors.RED,
        )
        raise typer.Abort()

    preset_choices = {
        preset.display_name: preset
        for preset in presets_in_category.values()
    }

    choice = questionary.select(
        f"Select {category_name.lower()} worksheet:",
        choices=list(preset_choices.keys()),
    ).ask()

    if choice is None:
        raise typer.Abort()

    return preset_choices[choice]


def build_language_preset_choices(language_name: str) -> dict[str, WorksheetPreset]:
    preset_choices: dict[str, WorksheetPreset] = {}

    for category_name, presets in LANGUAGE_CATEGORIES[language_name].items():
        for preset in presets.values():
            label = f"{category_name} — {preset.display_name}"
            preset_choices[label] = preset

    return preset_choices


def select_multiple_presets_for_language(language_name: str) -> list[WorksheetPreset]:
    presets_in_language = LANGUAGE_PRESET_GROUPS[language_name]

    if not presets_in_language:
        typer.secho(f"No presets available for {language_name}.", fg=typer.colors.RED)
        raise typer.Abort()

    preset_choices = build_language_preset_choices(language_name)

    while True:
        choices = questionary.checkbox(
            f"Select one or more {language_name.lower()} worksheets:",
            choices=list(preset_choices.keys()),
        ).ask()
        print(repr(choices))

        if choices is None:
            raise typer.Abort()

        if not choices:
            typer.secho("Please select at least one preset.", fg=typer.colors.RED)
            continue

        return [preset_choices[choice] for choice in choices]


def build_combined_preset(language_name: str, presets: list[WorksheetPreset]) -> WorksheetPreset:
    if not presets:
        raise ValueError("At least one preset is required to build a combined preset.")

    combined_prompts: list[PromptEntry | str] = []
    sections: list[WorksheetSection] = []

    for preset in presets:
        combined_prompts.extend(preset.prompts)
        sections.append(
            WorksheetSection(
                title=preset.display_name,
                prompts=tuple(preset.prompts),
            )
        )

    combined_id = "combined_" + "__".join(preset.id for preset in presets)
    combined_display_name = f"{language_name} Combined"

    return WorksheetPreset(
        id=combined_id,
        display_name=combined_display_name,
        prompts=tuple(combined_prompts),
        available_fonts=presets[0].available_fonts,
        guide_style=presets[0].guide_style,
        sections=tuple(sections),
    )


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
