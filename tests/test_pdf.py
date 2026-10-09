from pathlib import Path

import pytest

from handwriting_pdf_generator.domain.worksheet_preset import (
    GuideStyle,
    LogicalWorksheetPage,
    OutputLayoutMode,
    RowRenderMode,
    WorksheetPreset,
)
from handwriting_pdf_generator.pdf import document, fonts, generator, layout


def test_layout_defaults_and_derived_properties():
    page_layout = layout.build_single_page_layout(layout.PageOrientation.PORTRAIT, layout.FontSize.FOURTEEN)

    assert page_layout.page_orientation is layout.PageOrientation.PORTRAIT
    assert page_layout.page_width == layout.LETTER[0]
    assert page_layout.page_height == layout.LETTER[1]
    assert page_layout.line_height == page_layout.text_font_size + page_layout.line_gap
    assert page_layout.guide_cell_step == page_layout.guide_cell_width + page_layout.guide_cell_gap


def test_build_output_pdf_path_and_create_canvas(monkeypatch, tmp_path):
    class FakeDatetime:
        @staticmethod
        def now():
            class _Moment:
                @staticmethod
                def strftime(_fmt):
                    return "20260101_120000"

            return _Moment()

    monkeypatch.setattr(document, "datetime", FakeDatetime)

    pdf_path = document.build_output_pdf_path(str(tmp_path), "My Worksheet")
    assert pdf_path == tmp_path / "My Worksheet_20260101_120000.pdf"

    created = {}

    class FakeCanvas:
        def __init__(self, path, page_size):
            created["init"] = (path, page_size)

        def setTitle(self, title):
            created["title"] = title

    monkeypatch.setattr(document.canvas, "Canvas", FakeCanvas)

    page_layout = layout.build_single_page_layout(layout.PageOrientation.PORTRAIT, layout.FontSize.TWELVE)
    canvas_obj = document.create_canvas(pdf_path, "My Worksheet", page_layout)
    assert isinstance(canvas_obj, FakeCanvas)
    assert created["init"] == (str(pdf_path), page_layout.page_size)
    assert created["title"] == "My Worksheet"

    with pytest.raises(ValueError):
        document.create_canvas(tmp_path, "Bad", page_layout)


def test_register_font_uses_catalog_metadata(monkeypatch):
    captured = {}

    class FakeResource:
        def __init__(self, base):
            self.base = base

        def joinpath(self, *parts):
            captured["parts"] = parts
            return Path("/fake") / "/".join(parts)

    monkeypatch.setattr(fonts, "files", lambda _package: FakeResource("base"))
    monkeypatch.setattr(fonts.pdfmetrics, "registerFont", lambda font: captured.setdefault("registered", font))

    class FakeTTFont:
        def __init__(self, name, path):
            self.name = name
            self.path = path

    monkeypatch.setattr(fonts, "TTFont", FakeTTFont)

    font_name = fonts.register_font("noto_sans_jp")

    assert font_name == "NotoSansJP-VariableFont_wght.ttf"
    assert captured["parts"] == ("../assets/fonts", "Noto_Sans_JP", "NotoSansJP-VariableFont_wght.ttf")
    assert captured["registered"].name == "NotoSansJP-VariableFont_wght.ttf"


def test_generator_orchestrates_pdf_build(monkeypatch):
    preset = WorksheetPreset(
        id="sample",
        display_name="Sample Worksheet",
        prompts=("a", "b"),
        available_fonts=("font-id",),
        guide_style=GuideStyle.NONE,
    )
    calls = []
    single_page = LogicalWorksheetPage(title="Sample Worksheet", lines=("a", "b"))
    single_page_layout = layout.PageLayout(page_orientation=layout.PageOrientation.PORTRAIT, text_font_size=layout.FontSize.TWELVE)

    monkeypatch.setattr(generator, "build_output_pdf_path", lambda output_path, display_name: calls.append(("path", output_path, display_name)) or Path("/tmp/sample.pdf"))
    monkeypatch.setattr(generator, "register_font", lambda font_id: calls.append(("font", font_id)) or "FontName")
    monkeypatch.setattr(
        generator,
        "build_single_page_layout",
        lambda *, page_orientation, font_size: calls.append(("layout", page_orientation, font_size)) or single_page_layout,
    )

    class FakeCanvas:
        def save(self):
            calls.append(("save",))

    monkeypatch.setattr(generator, "create_canvas", lambda pdf_path, title, layout: calls.append(("canvas", pdf_path, title, layout)) or FakeCanvas())
    monkeypatch.setattr(generator, "plan_rows", lambda preset: calls.append(("plan_rows", preset.id)) or ["a", "b"])
    monkeypatch.setattr(generator, "paginate_lines", lambda preset, layout, lines: calls.append(("paginate_lines", preset.id, tuple(lines))) or [single_page])
    monkeypatch.setattr(generator, "set_page_characteristics", lambda pdf, font_name, layout: calls.append(("characteristics", font_name, layout)))
    monkeypatch.setattr(generator, "draw_title", lambda pdf, title, layout: calls.append(("title", title, layout)))
    monkeypatch.setattr(
        generator,
        "draw_lines_row_render_single",
        lambda pdf, prompts, layout, font_name, guide_style: calls.append(("lines_single", tuple(prompts), font_name, guide_style)),
    )
    monkeypatch.setattr(generator, "draw_lines_row_render_repeat", lambda *args: calls.append(("lines_repeat",)))

    generator.Generator(
        preset=preset,
        output_path="/out",
        row_render_mode=RowRenderMode.SINGLE,
        page_orientation=layout.PageOrientation.PORTRAIT,
        output_mode=OutputLayoutMode.SINGLE_PAGE,
        font_size=layout.FontSize.TWELVE,
    ).generate()

    assert calls == [
        ("path", "/out", "Sample Worksheet"),
        ("font", "font-id"),
        ("layout", layout.PageOrientation.PORTRAIT, layout.FontSize.TWELVE),
        ("canvas", Path("/tmp/sample.pdf"), "Sample Worksheet", single_page_layout),
        ("plan_rows", "sample"),
        ("paginate_lines", "sample", ("a", "b")),
        ("characteristics", "FontName", single_page_layout),
        ("title", "Sample Worksheet", single_page_layout),
        ("lines_single", ("a", "b"), "FontName", GuideStyle.NONE),
        ("save",),
    ]


def test_generator_imposes_booklet_pages_and_uses_repeat_renderer(monkeypatch):
    preset = WorksheetPreset(
        id="sample",
        display_name="Sample Worksheet",
        prompts=("a",),
        available_fonts=("font-id",),
        guide_style=GuideStyle.PLUS_DOTTED,
    )
    calls = []
    page = LogicalWorksheetPage(title="Sample Worksheet", lines=("a",))
    base_layout = layout.PageLayout(page_orientation=layout.PageOrientation.LANDSCAPE, text_font_size=layout.FontSize.FOURTEEN)
    booklet_layout = layout.PageLayout(
        page_orientation=layout.PageOrientation.PORTRAIT,
        base_page_size=layout.HALF_LETTER,
        text_font_size=layout.FontSize.FOURTEEN,
    )

    monkeypatch.setattr(generator, "build_output_pdf_path", lambda output_path, display_name: calls.append(("path", output_path, display_name)) or Path("/tmp/sample.pdf"))
    monkeypatch.setattr(generator, "register_font", lambda font_id: calls.append(("font", font_id)) or "FontName")
    monkeypatch.setattr(
        generator,
        "build_single_page_layout",
        lambda *, page_orientation, font_size: calls.append(("layout", page_orientation, font_size)) or base_layout,
    )

    class FakeCanvas:
        def saveState(self):
            calls.append(("saveState",))

        def translate(self, x, y):
            calls.append(("translate", x, y))

        def restoreState(self):
            calls.append(("restoreState",))

        def save(self):
            calls.append(("save",))

    monkeypatch.setattr(generator, "create_canvas", lambda pdf_path, title, layout: calls.append(("canvas", pdf_path, title, layout)) or FakeCanvas())
    monkeypatch.setattr(generator, "plan_rows", lambda preset: calls.append(("plan_rows", preset.id)) or ["a"])
    monkeypatch.setattr(generator, "paginate_lines", lambda preset, layout, lines: calls.append(("paginate_lines", preset.id, tuple(lines))) or [page])
    monkeypatch.setattr(generator, "impose_booklet_pages", lambda pages: calls.append(("impose_booklet_pages", tuple(pages))) or [page])
    monkeypatch.setattr(generator, "set_page_characteristics", lambda pdf, font_name, layout: calls.append(("characteristics", font_name, layout)))
    monkeypatch.setattr(generator, "build_booklet_page_one_layout", lambda initial_layout: calls.append(("booklet_layout", initial_layout)) or booklet_layout)
    monkeypatch.setattr(generator, "draw_title", lambda pdf, title, layout: calls.append(("title", title, layout)))
    monkeypatch.setattr(
        generator,
        "draw_lines_row_render_repeat",
        lambda pdf, prompts, layout, font_name, guide_style: calls.append(("lines_repeat", tuple(prompts), font_name, guide_style, layout)),
    )
    monkeypatch.setattr(generator, "draw_lines_row_render_single", lambda *args: calls.append(("lines_single",)))

    generator.Generator(
        preset=preset,
        output_path="/out",
        row_render_mode=RowRenderMode.REPEAT,
        page_orientation=layout.PageOrientation.LANDSCAPE,
        output_mode=OutputLayoutMode.BOOKLET,
        font_size=layout.FontSize.FOURTEEN,
    ).generate()

    assert calls == [
        ("path", "/out", "Sample Worksheet"),
        ("font", "font-id"),
        ("layout", layout.PageOrientation.LANDSCAPE, layout.FontSize.FOURTEEN),
        ("canvas", Path("/tmp/sample.pdf"), "Sample Worksheet", base_layout),
        ("plan_rows", "sample"),
        ("paginate_lines", "sample", ("a",)),
        ("impose_booklet_pages", (page,)),
        ("characteristics", "FontName", base_layout),
        ("booklet_layout", base_layout),
        ("saveState",),
        ("translate", base_layout.page_size[0] / 2, 0),
        ("title", "Sample Worksheet", booklet_layout),
        ("lines_repeat", ("a",), "FontName", GuideStyle.PLUS_DOTTED, booklet_layout),
        ("restoreState",),
        ("save",),
    ]
