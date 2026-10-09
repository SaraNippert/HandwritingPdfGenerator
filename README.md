# Handwriting PDF Generator

Generate printable handwriting-practice PDFs with lightly styled characters you can trace by hand.

This project is built around an interactive CLI and currently supports Japanese and French worksheet presets, plus booklet-style output for duplex printing.

## Features

- Interactive worksheet generation from preset character sets
- Japanese presets for hiragana, katakana, and kanji
- French lowercase worksheets
- Single-page or booklet output modes
- Repeat-row or single-character row rendering
- Configurable page orientation and tested font sizes
- Timestamped PDF output written to your Downloads folder by default

## Supported presets

The CLI currently exposes the following preset groups:

- **Japanese**
  - Katakana Gojuon
  - Katakana Dakuten / Handakuten
  - Hiragana Gojuon
  - Hiragana Dakuten / Handakuten
  - Kanji presets loaded from CSV files in `src/handwriting_pdf_generator/data/kanji/`
- **French**
  - French Lowercase

> Note: font choice is currently preset-driven. The CLI does not yet expose a free-form font picker.

## Requirements

- Python 3.12+
- `pip` or another Python package installer

## Quick start

### 1) Clone the repository

```bash
git clone https://github.com/SaraNippert/HandwritingPdfGenerator.git
cd HandwritingPdfGenerator
```

### 2) Create and activate a virtual environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 3) Install the project in editable mode

```bash
python -m pip install --upgrade pip
pip install -e .
```

### 4) Run the CLI

Use the installed command and the `generate` subcommand:

```bash
handwriting-pdf generate
```

Or run it as a module:

```bash
python -m handwriting_pdf_generator generate
```

If you want to see the available commands first, run:

```bash
handwriting-pdf --help
python -m handwriting_pdf_generator --help
```

### 5) Run the tests

```bash
pytest
```

## CLI workflow

When you start the generator, the app walks you through:

1. Choosing whether to build a single preset or combine multiple presets
2. Choosing a language group
3. Choosing the worksheet preset(s)
4. Selecting row rendering mode
5. Selecting output mode:
   - `single-page`
   - `booklet`
6. Selecting page orientation when booklet mode is not used
7. Selecting a tested font size

If booklet output is selected, the app prints a reminder to print **two pages per sheet, double-sided**.

## Output behavior

- PDFs are saved to `~/Downloads` by default
- Output filenames are timestamped, for example:

```text
Hiragana Gojuon_20261009_120102.pdf
```

- Booklet mode is designed for duplex printing and imposes pages into booklet order
- Single-page mode keeps the worksheet in normal page order

## Project structure

```text
HandwritingPdfGenerator/
├── pyproject.toml
├── README.md
├── src/
│   └── handwriting_pdf_generator/
│       ├── __main__.py
│       ├── entrypoint.py
│       ├── cli/
│       │   ├── app.py
│       │   ├── prompts.py
│       │   └── commands/
│       │       └── generate.py
│       ├── domain/
│       │   ├── worksheet_preset.py
│       │   └── font_catalog.py
│       ├── presets/
│       │   ├── french.py
│       │   ├── hiragana.py
│       │   ├── kanji.py
│       │   └── katakana.py
│       ├── pdf/
│       │   ├── booklet.py
│       │   ├── document.py
│       │   ├── fonts.py
│       │   ├── generator.py
│       │   ├── layout.py
│       │   ├── pagenation.py
│       │   └── renderer.py
│       └── data/
│           └── kanji/
└── tests/
```

## Adding fonts

1. Download the font you want to bundle.
2. Copy the font files into `src/handwriting_pdf_generator/assets/fonts/`.
3. Register the font in `src/handwriting_pdf_generator/domain/font_catalog.py`.
4. Update any preset that should use the new font.
5. Reinstall the package:

```bash
pip install -e .
```

## Adding kanji data

1. Add a new `.csv` file to `src/handwriting_pdf_generator/data/kanji/`
2. Put one character per line
3. Restart the CLI to pick up the new generated preset

## Roadmap

- Complete single-character worksheet handling
- Improve French cursive spacing
- Expand kanji preset coverage
- Add direct font selection in the CLI

## Development notes

- The package entry flow starts in `src/handwriting_pdf_generator/__main__.py`
- CLI prompts live in `src/handwriting_pdf_generator/cli/prompts.py`
- PDF generation is handled under `src/handwriting_pdf_generator/pdf/`
- Fonts are bundled with the package and registered through the font catalog
