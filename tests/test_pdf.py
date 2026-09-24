from pathlib import Path

import pytest

from handwriting_pdf_generator.domain.worksheet_preset import GuideStyle, RowRenderMode, WorksheetPreset
from handwriting_pdf_generator.pdf import document, fonts, generator, layout


def test_layout_defaults_and_derived_properties():
    page_layout = layout.build_single_page_layout()

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

    class FakeCanvas:
        def __init__(self, path, page_size):
            self.path = path
            self.page_size = page_size
            self.title = None

        def setTitle(self, title):
            self.title = title

    monkeypatch.setattr(document.canvas, "Canvas", FakeCanvas)

    canvas_obj = document.create_canvas(pdf_path, "My Worksheet", layout.build_single_page_layout())
    assert canvas_obj.path == str(pdf_path)
    assert canvas_obj.title == "My Worksheet"

    with pytest.raises(ValueError):
        document.create_canvas(tmp_path, "Bad", layout.build_single_page_layout())


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

    monkeypatch.setattr(generator, "build_output_pdf_path", lambda output_path, display_name: calls.append(("path", output_path, display_name)) or Path("/tmp/sample.pdf"))
    monkeypatch.setattr(generator, "register_font", lambda font_id: calls.append(("font", font_id)) or "FontName")
    monkeypatch.setattr(generator, "build_single_page_layout", lambda: calls.append(("layout",)) or layout.PageLayout())

    class FakeCanvas:
        def save(self):
            calls.append(("save",))

    monkeypatch.setattr(generator, "create_canvas", lambda pdf_path, title, layout: calls.append(("canvas", pdf_path, title, layout)) or FakeCanvas())
    monkeypatch.setattr(generator, "draw_title", lambda *args: calls.append(("title", args[1])))
    monkeypatch.setattr(generator, "draw_character_lines", lambda *args: calls.append(("lines", args[1], args[4], args[5])))

    generator.Generator(preset=preset, output_path="/out", row_render_mode=RowRenderMode.SINGLE).generate()

    assert calls == [
        ("path", "/out", "Sample Worksheet"),
        ("font", "font-id"),
        ("layout",),
        ("canvas", Path("/tmp/sample.pdf"), "Sample Worksheet", layout.PageLayout()),
        ("title", "Sample Worksheet"),
        ("lines", ("a", "b"), RowRenderMode.SINGLE, GuideStyle.NONE),
        ("save",),
    ]
