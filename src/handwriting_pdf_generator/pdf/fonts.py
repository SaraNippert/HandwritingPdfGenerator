from importlib.resources import files
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from ..domain.font_catalog import ALL_FONTS

def register_font(font_id: str) -> str:
    """Register bundled Japanese font and return its ReportLab name."""

    # Find font information from the catalog
    selected_font = ALL_FONTS[font_id]
    font_file = selected_font.file_name
    font_directory = selected_font.font_directory

    font_path = files(__package__).joinpath("../assets/fonts", font_directory, font_file)
    pdfmetrics.registerFont(TTFont(font_file, str(font_path)))
    return font_file
