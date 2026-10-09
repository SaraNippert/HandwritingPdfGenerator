from handwriting_pdf_generator.domain.worksheet_preset import LogicalWorksheetPage, WorksheetPreset, WorksheetSection
from handwriting_pdf_generator.pdf import booklet, layout, pagenation


def test_plan_rows_strips_blank_prompts():
    preset = WorksheetPreset(
        id="sample",
        display_name="Sample",
        prompts=(" a ", "", "b", "   "),
        available_fonts=("font-id",),
    )

    assert pagenation.plan_rows(preset) == ["a", "b"]


def test_paginate_lines_uses_sections_and_splits_pages():
    worksheet_layout = layout.PageLayout(
        page_orientation=layout.PageOrientation.LANDSCAPE,
        base_page_size=(100, 30),
        margin_top=5,
        margin_bottom=5,
        text_font_size=10,
        line_gap=0,
    )
    preset = WorksheetPreset(
        id="sample",
        display_name="Sample Worksheet",
        prompts=(),
        available_fonts=("font-id",),
        sections=(
            WorksheetSection(title="Part 1", prompts=("a", "b", "", "c")),
            WorksheetSection(title="Part 2", prompts=("d",)),
        ),
    )

    pages = pagenation.paginate_lines(preset, worksheet_layout, ["ignored"])

    assert pages == [
        LogicalWorksheetPage(title="Part 1", lines=("a", "b")),
        LogicalWorksheetPage(title="", lines=("c",)),
        LogicalWorksheetPage(title="Part 2", lines=("d",)),
    ]


def test_impose_booklet_pages_pads_and_reorders_pages():
    pages = ["p1", "p2", "p3", "p4", "p5"]

    assert booklet.impose_booklet_pages(pages) == [
        None,
        None,
        "p1",
        None,
        "p5",
        "p2",
        "p3",
        "p4",
    ]


