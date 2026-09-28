"""
 This file orchestrates the generation script
"""

import typer

from ..prompts import (
    header,
    select_worksheet_preset,
    select_row_render_mode,
    select_page_orientation,
    select_output_mode
)
from ...domain.worksheet_preset import OutputLayoutMode
from ...pdf.generator import Generator
from ...pdf.layout import PageOrientation


def handwriting_pdf() -> None:
    """Run the interactive CLI flow for selecting PDF options.

    This function:
    1. Prints a styled CLI header.
    2. Prompts the user to choose a worksheet preset.
    3. Prompts for row type (repeated or single characters).
    4. Prompts for page orientation (landscape or portrait).
    5. Prompts for output mode (booklet or standard).
    4. Generates a PDF given the user selections.
    """

    header()
    worksheet_selection = select_worksheet_preset()
    row_render_mode = select_row_render_mode()
    output_mode = select_output_mode()
    # booklets may only be landscape
    if output_mode == OutputLayoutMode.BOOKLET:
        page_orientation = PageOrientation.LANDSCAPE
    else:
        page_orientation = select_page_orientation()

    generator = Generator(
        preset=worksheet_selection,
        row_render_mode=row_render_mode,
        page_orientation=page_orientation,
        output_mode=output_mode
    )
    generator.generate()
