# Handwriting PDF Generator
This is a project to generate PDFs with grayed out characters to trace for handwriting practice.

I am particular about the handwriting sheets I like to use and this allows me to generate them how 
I'd like for my own personal notebook which is an A5 travelers notebook.
The A5 size allows me to print four sheets per letter-sized page, fold the pages in half, 
and create signatures to be used in the notebook.
I will eventually add support for other formats, mostly dependent on if I change which notebook I am using.

## Implementation Notes:
- Because this is intended for handwriting practice, not memorization and learning, the worksheets generated do not contain blank boxes or lines or stroke order guides.
- I prefer to write smaller, so the default worksheets generated use smaller characters than may be typical.
- I am printing to create signatures, which means the default order of the pages is arranged for this booklet style printing.

## Supported Languages/Characters
This app currently supports generating sheets for the following:
- Katakana
- Hiragana
- French cursive (appears, but not complete)

## To Do
- [ ] Add layout for two pages per sheet
- [ ] Add booklet printing
- [ ] Fix French cursive spacing
- [ ] Add support for Kanji
- [ ] Add font choices

## Guide
If you're new to programming, this section is for you.  
This project creates handwriting-practice PDFs, and you can customize it for your own notebook format, language set, and font preferences.

---

### Run locally

#### 1) Prerequisites
- Python 3.11+ (or your currently supported project version)
- `pipx` installed (recommended for running the CLI tool)

Install pipx guide:  
https://packaging.python.org/en/latest/guides/installing-stand-alone-command-line-tools/#installing-stand-alone-command-line-tools

#### 2) Clone and install for development

```bash
git clone <your-repo-url>
cd HandwritingPdfGenerator

python3 --version
python3 -m venv .venv
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -e .
```

#### 3) Verify with tests
```bash
pytest tests/
```

#### 4) Run the application
```bash
python -m handwriting_pdf_generator
```

Because this project uses a package entry point, run it as a module:
```bash
python -m handwriting_pdf_generator
```
You can also run the installed CLI command (if available in your environment):
```bash
handwriting-pdf-generator
```

##### Reinstall while actively developing

If you are using pipx and want to refresh your editable install after changes:
```bash
pipx uninstall handwriting-pdf-generator
pipx install -e .
```

### Project walkthrough
A good place to start is the package entry flow:
- src/handwriting_pdf_generator/__main__.py
- src/handwriting_pdf_generator/entrypoint.py
- src/handwriting_pdf_generator/cli/app.py

From there, follow the path:
1. CLI command handling (cli/)
2. preset/domain models (presets/, domain/)
3. PDF generation (pdf/)

#### Architecture

```text
HandwritingPdfGenerator/
├── pyproject.toml
├── README.md
├── src/
│   └── handwriting_pdf_generator/
│       ├── __init__.py
│       ├── __main__.py
│       ├── entrypoint.py
│       │
│       ├── cli/                      # command-line interface (Typer + prompts)
│       │   ├── app.py
│       │   ├── prompts.py
│       │   └── commands/
│       │       └── generate.py
│       │
│       ├── domain/                   # shared data models / core concepts
│       │   ├── worksheet_preset.py
│       │   └── font_catalog.py
│       │
│       ├── presets/                  # predefined character sets/configs
│       │   ├── hiragana.py
│       │   ├── katakana.py
│       │   └── french.py
│       │
│       ├── pdf/                      # PDF creation and rendering logic
│       │   ├── generator.py
│       │   ├── document.py
│       │   ├── fonts.py
│       │   ├── layout.py
│       │   ├── renderer.py
│       │   └── booklet.py
│       │
│       └── assets/
│           └── fonts/                # bundled font files used by ReportLab
│
└── tests/                            # test suite
```

#### Adding fonts
1. Find and download a font (Google Fonts is a good source): https://fonts.google.com/
2. Unzip the font locally.
3. Copy the font folder into: src/handwriting_pdf_generator/assets/fonts/
4. Register/update the font entry in: src/handwriting_pdf_generator/domain/font_catalog.py
5. Reinstall the package (especially if using pipx):
```bash
pipx uninstall handwriting-pdf-generator
pipx install -e .
```
After that, the font should appear as a selectable option in the app.