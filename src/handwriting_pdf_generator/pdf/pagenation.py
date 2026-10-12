# handles determining which content goes on which page (content slicing policy)
from reportlab.pdfbase.pdfmetrics import stringWidth

from ..domain.worksheet_preset import (
    WorksheetPreset,
    LogicalWorksheetPage,
    PromptEntry,
)
from ..pdf.layout import PageLayout


def _normalize_prompt_value(prompt: str | PromptEntry) -> PromptEntry | None:
    """Return a cleaned PromptEntry or None when text is blank."""
    if isinstance(prompt, PromptEntry):
        text = prompt.text.strip()
        definition = prompt.definition.strip()
    else:
        text = prompt.strip()
        definition = ""

    if not text:
        return None

    return PromptEntry(text=text, definition=definition)


def plan_rows(
        preset: WorksheetPreset,
) -> list[PromptEntry]:
    """
    stubbed for now - implement later
    :param preset:
    :return:
    """

    rows: list[PromptEntry] = []

    for prompt in preset.prompts:
        normalized = _normalize_prompt_value(prompt)
        if normalized is not None:
            rows.append(normalized)

    return rows

def _definition_font_size(layout: PageLayout) -> int:
    return min(layout.text_font_size, 12)

def _wrap_text_to_width(text: str, font_name: str, font_size: int, max_width: float) -> list[str]:
    words = text.split()
    if not words:
        return []

    lines: list[str] = []
    current = words[0]

    for word in words[1:]:
        candidate = f"{current} {word}"
        if stringWidth(candidate, font_name, font_size) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word

    lines.append(current)
    return lines


def _definition_line_count(
        entry: PromptEntry,
        layout: PageLayout,
        font_name: str,
) -> int:
    definition = entry.definition.strip()
    if not definition:
        return 0

    wrapped = _wrap_text_to_width(
        definition,
        font_name,
        _definition_font_size(layout),
        layout.right - layout.left,
    )
    return max(1, len(wrapped))

def _row_height_units(
        entry: PromptEntry,
        layout: PageLayout,
        font_name: str,
) -> int:
    # 1 line for the practice row itself, plus wrapped definition lines.
    return 1 + _definition_line_count(entry, layout, font_name)



def _paginate_prompt_entries(
        title: str,
        entries: list[PromptEntry],
        max_rows_per_page: int,
        layout: PageLayout,
        font_name: str,
) -> list[LogicalWorksheetPage]:
    pages: list[LogicalWorksheetPage] = []

    if max_rows_per_page <= 0:
        return pages

    current_page: list[PromptEntry] = []
    current_units = 0
    is_first_page = True

    for entry in entries:
        entry_units = _row_height_units(entry, layout, font_name)

        if current_page and current_units + entry_units > max_rows_per_page:
            pages.append(
                LogicalWorksheetPage(
                    title=title if is_first_page else "",
                    lines=tuple(current_page),
                )
            )
            current_page = []
            current_units = 0
            is_first_page = False

        current_page.append(entry)
        current_units += entry_units

    if current_page:
        pages.append(
            LogicalWorksheetPage(
                title=title if is_first_page else "",
                lines=tuple(current_page),
            )
        )

    return pages


def paginate_lines(
        preset: WorksheetPreset,
        layout: PageLayout,
        lines: list[PromptEntry],
        font_name: str,
) -> list[LogicalWorksheetPage]:
    """
    Paginate normalized PromptEntry rows into logical worksheet pages.

    Note:
    - Section prompts are still treated as plain strings in this version.
    - Non-section flow uses normalized prompt entries and preserves current output shape.
    """
    if preset.sections:
        pages: list[LogicalWorksheetPage] = []

        for section in preset.sections:
            section_lines: list[PromptEntry] = []
            for prompt in section.prompts:
                normalized = _normalize_prompt_value(prompt)
                if normalized is not None:
                    section_lines.append(normalized)

            pages.extend(
                _paginate_prompt_entries(
                    title=section.title,
                    entries=section_lines,
                    max_rows_per_page=layout.max_rows_per_page,
                    layout=layout,
                    font_name=font_name,
                )
            )

        return pages

    return _paginate_prompt_entries(
        title=preset.display_name,
        entries=lines,
        max_rows_per_page=layout.max_rows_per_page,
        layout=layout,
        font_name=font_name,
    )