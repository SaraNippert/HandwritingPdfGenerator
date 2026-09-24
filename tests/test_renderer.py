import importlib

import pytest


worksheet_preset = importlib.import_module("handwriting_pdf_generator.domain.worksheet_preset")
renderer = importlib.import_module("handwriting_pdf_generator.pdf.renderer")
PageLayout = importlib.import_module("handwriting_pdf_generator.pdf.layout").PageLayout
GuideStyle = worksheet_preset.GuideStyle
RowRenderMode = worksheet_preset.RowRenderMode


class FakeCanvas:
    def __init__(self):
        self.calls = []

    def setFont(self, font_name, size):
        self.calls.append(("setFont", font_name, size))

    def drawString(self, x, y, text):
        self.calls.append(("drawString", x, y, text))

    def setFillColor(self, color):
        self.calls.append(("setFillColor", color))

    def showPage(self):
        self.calls.append(("showPage",))


def test_draw_title_places_title_using_layout_offsets():
    pdf = FakeCanvas()
    page_layout = PageLayout(page_size=(200, 300), margin_left=12, margin_top=20, title_top_offset=8)

    renderer.draw_title(pdf, "Worksheet", page_layout, "MyFont")

    assert pdf.calls == [
        ("setFont", "MyFont", page_layout.title_font_size),
        ("drawString", page_layout.left, page_layout.top - page_layout.title_top_offset, "Worksheet"),
    ]


def test_draw_character_lines_plain_repeat_advances_by_token_width(monkeypatch):
    pdf = FakeCanvas()
    page_layout = PageLayout(page_size=(100, 100), margin_left=10, margin_right=10, text_font_size=10, line_gap=0)
    monkeypatch.setattr(renderer, "stringWidth", lambda text, font_name, size: 20)

    renderer.draw_character_lines(
        pdf,
        ["ab"],
        page_layout,
        "MyFont",
        RowRenderMode.REPEAT,
        GuideStyle.NONE,
    )

    assert pdf.calls[0] == ("setFont", "MyFont", page_layout.text_font_size)
    assert pdf.calls[1][0] == "setFillColor"
    assert [call[0] for call in pdf.calls[2:]] == ["drawString", "drawString", "drawString", "drawString"]
    assert [call[1] for call in pdf.calls[2:]] == [10, 30, 50, 70]


def test_draw_character_lines_plus_dotted_single_centers_text(monkeypatch):
    pdf = FakeCanvas()
    page_layout = PageLayout(page_size=(100, 100), margin_left=10, text_font_size=10, line_gap=0)
    monkeypatch.setattr(renderer, "stringWidth", lambda text, font_name, size: 8)

    guide_calls = []
    monkeypatch.setattr(
        renderer,
        "_draw_dotted_plus_cell",
        lambda pdf_obj, x, y, cell_w, cell_h, layout_obj: guide_calls.append((x, y, cell_w, cell_h)),
    )

    renderer.draw_character_lines(
        pdf,
        ["a"],
        page_layout,
        "MyFont",
        RowRenderMode.SINGLE,
        GuideStyle.PLUS_DOTTED,
    )

    assert guide_calls == [(page_layout.left, page_layout.first_row_baseline, page_layout.guide_cell_width, page_layout.guide_cell_height)]
    assert pdf.calls[-1] == ("drawString", page_layout.left + (page_layout.guide_cell_width - 8) / 2, page_layout.first_row_baseline, "a")


def test_draw_character_lines_rejects_unsupported_guide_style(monkeypatch):
    pdf = FakeCanvas()
    page_layout = PageLayout(page_size=(100, 100))
    monkeypatch.setattr(renderer, "stringWidth", lambda text, font_name, size: 10)

    with pytest.raises(ValueError, match="Unsupported guide style"):
        renderer.draw_character_lines(pdf, ["a"], page_layout, "MyFont", RowRenderMode.SINGLE, "bad-style")
