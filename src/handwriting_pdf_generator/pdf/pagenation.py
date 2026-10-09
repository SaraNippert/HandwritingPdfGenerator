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
    if preset.sections:
        pages: list[LogicalWorksheetPage] = []

        for section in preset.sections:
            section_lines = [prompt.strip() for prompt in section.prompts if prompt.strip()]
            number_of_lines = len(section_lines)
            total_pages = math.ceil(number_of_lines / layout.max_rows_per_page)

            for index in range(total_pages):
                title = section.title if index == 0 else ""
                page_lines = section_lines[
                    index * layout.max_rows_per_page:(index + 1) * layout.max_rows_per_page
                ]

                pages.append(
                    LogicalWorksheetPage(
                        title=title,
                        lines=tuple(page_lines),
                    )
                )

        return pages

    pages = []

    number_of_lines = len(lines)
    total_pages = math.ceil(number_of_lines / layout.max_rows_per_page)

    for index in range(total_pages):
        title = preset.display_name if index == 0 else ""
        page_lines = lines[index * layout.max_rows_per_page:(index + 1) * layout.max_rows_per_page]

        pages.append(
            LogicalWorksheetPage(
                title=title,
                lines=tuple(page_lines),
            )
        )

    return pages
