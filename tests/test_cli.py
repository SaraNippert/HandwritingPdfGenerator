import pytest
import typer

from handwriting_pdf_generator.cli import prompts
from handwriting_pdf_generator.cli.commands import generate as generate_module
from handwriting_pdf_generator.cli.commands.generate import handwriting_pdf
from handwriting_pdf_generator.domain.worksheet_preset import OutputLayoutMode, RowRenderMode
from handwriting_pdf_generator.pdf.layout import FontSize, PageOrientation


class _FakePrompt:
    def __init__(self, result):
        self.result = result

    def ask(self):
        return self.result


def test_select_worksheet_preset_returns_selected_preset(monkeypatch):
    monkeypatch.setattr(prompts, "select_preset_selection_mode", lambda: prompts.PresetSelectionMode.SINGLE)
    monkeypatch.setattr(prompts, "select_language", lambda: "Japanese")
    monkeypatch.setattr(prompts, "select_category", lambda language_name: "Katakana")
    monkeypatch.setattr(
        prompts,
        "select_single_preset_from_category",
        lambda language_name, category_name: prompts.KATAKANA_PRESETS["katakana_gojuon"],
    )

    preset = prompts.select_worksheet_preset()

    assert preset.id == "katakana_gojuon"
    assert preset.display_name == "Katakana Gojuon"


def test_select_worksheet_preset_combines_selected_presets(monkeypatch):
    monkeypatch.setattr(prompts, "select_preset_selection_mode", lambda: prompts.PresetSelectionMode.COMBINE)
    monkeypatch.setattr(prompts, "select_language", lambda: "French")
    monkeypatch.setattr(
        prompts,
        "select_multiple_presets_for_language",
        lambda language_name: [prompts.FRENCH_PRESETS["french_lowercase"]],
    )

    preset = prompts.select_worksheet_preset()

    assert preset.id == "combined_french_lowercase"
    assert preset.display_name == "French Combined"
    assert preset.prompts == prompts.FRENCH_PRESETS["french_lowercase"].prompts


def test_select_worksheet_preset_abort_on_cancel(monkeypatch):
    monkeypatch.setattr(prompts.questionary, "select", lambda *args, **kwargs: _FakePrompt(None))

    with pytest.raises(typer.Abort):
        prompts.select_worksheet_preset()


def test_select_row_render_mode_defaults_to_repeat(monkeypatch):
    monkeypatch.setattr(prompts.questionary, "select", lambda *args, **kwargs: _FakePrompt(None))

    assert prompts.select_row_render_mode() is RowRenderMode.REPEAT


def test_handwriting_pdf_runs_single_page_generator_flow(monkeypatch):
    calls = []

    monkeypatch.setattr(generate_module, "header", lambda: calls.append("header"))
    monkeypatch.setattr(
        generate_module,
        "select_worksheet_preset",
        lambda: calls.append("preset") or prompts.FRENCH_PRESETS["french_lowercase"],
    )
    monkeypatch.setattr(generate_module, "select_row_render_mode", lambda: calls.append("mode") or RowRenderMode.SINGLE)
    monkeypatch.setattr(generate_module, "select_output_mode", lambda: calls.append("output") or OutputLayoutMode.SINGLE_PAGE)
    monkeypatch.setattr(generate_module, "select_page_orientation", lambda: calls.append("orientation") or PageOrientation.PORTRAIT)
    monkeypatch.setattr(generate_module, "select_font_size", lambda: calls.append("font_size") or FontSize.TWELVE)
    monkeypatch.setattr(generate_module, "booklet_instructions", lambda: calls.append("booklet_instructions"))

    class FakeGenerator:
        def __init__(self, *, preset, row_render_mode, page_orientation, output_mode, font_size):
            calls.append((preset.id, row_render_mode, page_orientation, output_mode, font_size))

        def generate(self):
            calls.append("generate")

    monkeypatch.setattr(generate_module, "Generator", FakeGenerator)

    handwriting_pdf()

    assert calls == [
        "header",
        "preset",
        "mode",
        "output",
        "orientation",
        "font_size",
        ("french_lowercase", RowRenderMode.SINGLE, PageOrientation.PORTRAIT, OutputLayoutMode.SINGLE_PAGE, FontSize.TWELVE),
        "generate",
    ]


def test_handwriting_pdf_uses_landscape_booklet_and_prints_instructions(monkeypatch):
    calls = []

    monkeypatch.setattr(generate_module, "header", lambda: calls.append("header"))
    monkeypatch.setattr(
        generate_module,
        "select_worksheet_preset",
        lambda: calls.append("preset") or prompts.FRENCH_PRESETS["french_lowercase"],
    )
    monkeypatch.setattr(generate_module, "select_row_render_mode", lambda: calls.append("mode") or RowRenderMode.REPEAT)
    monkeypatch.setattr(generate_module, "select_output_mode", lambda: calls.append("output") or OutputLayoutMode.BOOKLET)
    monkeypatch.setattr(generate_module, "select_page_orientation", lambda: calls.append("orientation"))
    monkeypatch.setattr(generate_module, "select_font_size", lambda: calls.append("font_size") or FontSize.FOURTEEN)
    monkeypatch.setattr(generate_module, "booklet_instructions", lambda: calls.append("booklet_instructions"))

    class FakeGenerator:
        def __init__(self, *, preset, row_render_mode, page_orientation, output_mode, font_size):
            calls.append((preset.id, row_render_mode, page_orientation, output_mode, font_size))

        def generate(self):
            calls.append("generate")

    monkeypatch.setattr(generate_module, "Generator", FakeGenerator)

    handwriting_pdf()

    assert calls == [
        "header",
        "preset",
        "mode",
        "output",
        "font_size",
        ("french_lowercase", RowRenderMode.REPEAT, PageOrientation.LANDSCAPE, OutputLayoutMode.BOOKLET, FontSize.FOURTEEN),
        "generate",
        "booklet_instructions",
    ]

