import pytest
import typer

from handwriting_pdf_generator.cli.app import app
from handwriting_pdf_generator.cli.commands.generate import handwriting_pdf
from handwriting_pdf_generator.cli import prompts
from handwriting_pdf_generator.cli.commands import generate as generate_module
from handwriting_pdf_generator.domain.worksheet_preset import RowRenderMode


class _FakePrompt:
    def __init__(self, result):
        self.result = result

    def ask(self):
        return self.result


def test_app_registers_generate_command():
    assert app.registered_commands[0].name == "generate"


def test_select_worksheet_preset_returns_selected_preset(monkeypatch):
    monkeypatch.setattr(prompts.questionary, "select", lambda *args, **kwargs: _FakePrompt("katakana_grid"))

    preset = prompts.select_worksheet_preset()

    assert preset.id == "katakana_grid"
    assert preset.display_name == "Katakana Grid"


def test_select_worksheet_preset_abort_on_cancel(monkeypatch):
    monkeypatch.setattr(prompts.questionary, "select", lambda *args, **kwargs: _FakePrompt(None))

    with pytest.raises(typer.Abort):
        prompts.select_worksheet_preset()


def test_select_row_render_mode_defaults_to_repeat(monkeypatch):
    monkeypatch.setattr(prompts.questionary, "select", lambda *args, **kwargs: _FakePrompt(None))

    assert prompts.select_row_render_mode() is RowRenderMode.REPEAT


def test_handwriting_pdf_runs_generator_flow(monkeypatch):
    calls = []

    monkeypatch.setattr(generate_module, "header", lambda: calls.append("header"))
    monkeypatch.setattr(generate_module, "select_worksheet_preset", lambda: calls.append("preset") or prompts.ALL_PRESETS["french_lowercase"])
    monkeypatch.setattr(generate_module, "select_row_render_mode", lambda: calls.append("mode") or RowRenderMode.SINGLE)

    class FakeGenerator:
        def __init__(self, preset, row_render_mode):
            calls.append((preset.id, row_render_mode))

        def generate(self):
            calls.append("generate")

    monkeypatch.setattr(generate_module, "Generator", FakeGenerator)

    handwriting_pdf()

    assert calls == ["header", "preset", "mode", ("french_lowercase", RowRenderMode.SINGLE), "generate"]

