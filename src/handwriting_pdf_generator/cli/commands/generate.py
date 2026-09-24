"""
 This file orchestrates the generation script
"""

import typer

from ..prompts import header, select_worksheet_preset, select_row_render_mode
from ...pdf.generator import Generator

def handwriting_pdf() -> None:
    """Run the interactive CLI flow for selecting PDF options.

    This function:
    1. Prints a styled CLI header.
    2. Prompts the user to choose a PDF type from a keyboard-navigable list.
    3. Prompts for the output PDF name.
    4. Echoes the selected values.
    """

    header()

    # user selects PDF type
    worksheet_selection = select_worksheet_preset()
    typer.echo(f"Worksheet Selection: {worksheet_selection.id}")

    row_render_mode = select_row_render_mode()
    typer.echo(f"Row Render Mode: {row_render_mode}")

    generator = Generator(preset=worksheet_selection, row_render_mode=row_render_mode)
    generator.generate()



