# document-level setup (page size/margins)

from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from ..pdf.layout import PageLayout

DEFAULT_OUTPUT_PATH = Path.home() / "Downloads"

def build_output_pdf_path(output_dir: str, display_name: str) -> Path:
    """
       Build the full output path for a generated PDF file.

       Creates the output directory (and any missing parent directories) if it
       does not already exist, then returns the target PDF path using the
       provided display name and a `.pdf` extension.

       Args:
           output_dir: Directory where generated PDFs should be written.
           display_name: Base filename to use for the PDF (without extension).

       Returns:
           A `Path` object pointing to `<output_dir>/<display_name>.pdf`.
       """
    base_dir = Path(output_dir)
    base_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return base_dir / f"{display_name}_{timestamp}.pdf"

def create_canvas(pdf_path: Path, title: str, layout: PageLayout) -> canvas.Canvas:
    """
    Create a ReportLab canvas for a full output PDF path and set document title.

    Raises:
        ValueError: If pdf_path does not appear to point to a .pdf file.
        OSError: If the file cannot be opened/written due to filesystem issues.
        RuntimeError: If canvas creation fails for non-filesystem reasons.
    """
    try:
        # Validate expected input shape early (fail fast).
        if pdf_path.suffix.lower() != ".pdf":
            raise ValueError("pdf_path must include a .pdf filename, not just a directory")

        pdf = canvas.Canvas(str(pdf_path), layout.page_size)
        pdf.setTitle(title)
        return pdf

    except ValueError:
        raise
    except OSError:
        raise
    except Exception as exc:
        raise RuntimeError(f"Failed to create PDF canvas for '{pdf_path}'") from exc
