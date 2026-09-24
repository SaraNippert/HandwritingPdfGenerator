# handles determining which content goes on which page (content slicing policy)
import math
from reportlab.pdfbase.pdfmetrics import stringWidth

from ..domain.worksheet_preset import (
    WorksheetPreset,
    LogicalWorksheetPage,
    RowRenderMode,
    GuideStyle
)
from ..pdf.layout import PageLayout


def plan_rows(
        preset: WorksheetPreset,
) -> list[str]:
    """
    stubbed for now - implement later
    :param preset:
    :return:
    """

    lines: list[str] = []

    for prompt in preset.prompts:
        text = prompt.strip()
        if text:
            lines.append(text)

    return lines


def paginate_lines(preset: WorksheetPreset, layout: PageLayout, lines: list[str]) -> list[LogicalWorksheetPage]:
    pages = []

    # determine how many lines can fit on a page
    # total available height of page divided by line height - round to whole number
    number_of_lines = len(lines)
    total_pages = math.ceil(number_of_lines / layout.max_rows_per_page)

    # create one worksheet for each group of lines
    for index in range(total_pages):

        # for now, only include title on first page
        if index == 0:
            title = preset.display_name
        else:
            title = ""

        page_lines = lines[index * layout.max_rows_per_page: (index + 1) * layout.max_rows_per_page]

        pages.append(LogicalWorksheetPage(
            title=title,
            lines=page_lines
        ))

    return pages
