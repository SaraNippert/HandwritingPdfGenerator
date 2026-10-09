from __future__ import annotations

from importlib.resources import files
from pathlib import Path

from ..domain.font_catalog import JAPANESE_FONT_LIST
from ..domain.worksheet_preset import GuideStyle, WorksheetPreset


def _label_from_stem(stem: str) -> str:
    """Convert a file stem like 'joyo-kanji' into 'Joyo Kanji'."""
    return stem.replace("_", " ").replace("-", " ").title()


def _preset_id_from_stem(stem: str) -> str:
    """Convert a file stem into a stable preset id."""
    normalized = stem.replace("-", "_").replace(" ", "_")
    return f"kanji_{normalized}"


def _load_kanji_csv(csv_path: Path) -> tuple[str, ...]:
    """
    Load one kanji per line from a CSV/text file.

    Blank lines are ignored.
    """
    lines = csv_path.read_text(encoding="utf-8").splitlines()
    prompts = tuple(line.strip() for line in lines if line.strip())
    return prompts


def load_kanji_presets() -> dict[str, WorksheetPreset]:
    """
    Discover all kanji CSV files bundled under data/kanji and convert them
    into WorksheetPreset objects.
    """
    kanji_dir = files("handwriting_pdf_generator").joinpath("data", "kanji")

    presets: dict[str, WorksheetPreset] = {}

    for resource in sorted(kanji_dir.iterdir(), key=lambda item: item.name):
        if resource.name.startswith("."):
            continue
        if not resource.name.lower().endswith(".csv"):
            continue

        stem = resource.name[:-4]
        preset_id = _preset_id_from_stem(stem)
        display_name = _label_from_stem(stem)

        prompts = _load_kanji_csv(Path(str(resource)))

        presets[preset_id] = WorksheetPreset(
            id=preset_id,
            display_name=display_name,
            prompts=prompts,
            available_fonts=tuple(JAPANESE_FONT_LIST),
            guide_style=GuideStyle.PLUS_DOTTED,
        )

    return presets


KANJI_PRESETS: dict[str, WorksheetPreset] = load_kanji_presets()