# draw glyphs, guides, styling
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib import colors
from reportlab.pdfgen.canvas import Canvas

from ..domain.worksheet_preset import RowRenderMode, GuideStyle
from ..pdf.layout import PageLayout


def draw_title(pdf, title: str, layout: PageLayout, font_name: str) -> None:
    """
    Draw the worksheet title at the configured title position.

    The title is placed at the left page margin (`layout.left`) and at a vertical
    position derived from the top boundary (`layout.top`) minus
    `layout.title_top_offset`.

    Args:
        pdf: ReportLab canvas object used for drawing.
        title: Text to render as the page title.
        layout: Page layout containing title coordinates and font settings.
        font_name: Name of the font to use for the title text.
    """
    pdf.setFont(font_name, layout.title_font_size)

    title_x = layout.left
    title_y = layout.top - layout.title_top_offset

    pdf.drawString(title_x, title_y, title)


# TODO: This method needs broken up
def draw_character_lines(
        pdf: Canvas,
        lines: list[str],
        layout: PageLayout,
        font_name: str,
        row_render_mode: RowRenderMode,
        guide_style: GuideStyle,
) -> None:
    """
    Draw worksheet practice rows for the provided text lines.

    This renderer supports two orthogonal dimensions of behavior:
    - Guide style:
      - `GuideStyle.PLUS_DOTTED`: draw guide cells with center cross lines.
      - `GuideStyle.NONE`: draw plain text only.
    - Row render mode:
      - `RowRenderMode.SINGLE`: draw one token/cell per row.
      - `RowRenderMode.REPEAT`: repeat token/cell horizontally until `layout.right`.

    Args:
        pdf: ReportLab canvas object used for drawing.
        lines: Text lines to render, one row per item.
        layout: Page layout containing text origin, boundaries, spacing, and style.
        font_name: Font name used for line text.
        row_render_mode: Controls single vs repeated row rendering behavior.
        guide_style: Controls whether and how guide cells are drawn.

    Raises:
        ValueError: If `row_render_mode` or `guide_style` is unsupported.
    """

    pdf = _set_page_characteristics(pdf, font_name, layout)

    line_height = layout.line_height
    y = layout.first_row_baseline

    for line_text in lines:
        if not line_text:
            y -= line_height
            continue

        # If we have reached the bottom of the page, start a new page
        if y <= (layout.bottom - line_height):
            pdf = _start_new_page(pdf, font_name, layout)
            y = layout.first_row_baseline

        x = layout.left
        token_width = stringWidth(line_text, font_name, layout.text_font_size)

        if token_width <= 0:
            y -= line_height
            continue

        if guide_style is GuideStyle.PLUS_DOTTED:
            if row_render_mode is RowRenderMode.SINGLE:
                _draw_dotted_plus_cell(pdf, x, y, layout.guide_cell_width, layout.guide_cell_height, layout)
                text_x = x + (layout.guide_cell_width - token_width) / 2
                pdf.drawString(text_x, y, line_text)
                y -= line_height
                continue

            if row_render_mode is RowRenderMode.REPEAT:
                while x + layout.guide_cell_width <= layout.right:
                    _draw_dotted_plus_cell(pdf, x, y, layout.guide_cell_width, layout.guide_cell_height, layout)
                    text_x = x + (layout.guide_cell_width - token_width) / 2
                    pdf.drawString(text_x, y, line_text)
                    x += layout.guide_cell_step

                y -= line_height
                continue

            raise ValueError(f"Unsupported row render mode: {row_render_mode}")

        if guide_style is GuideStyle.NONE:
            if row_render_mode is RowRenderMode.SINGLE:
                pdf.drawString(x, y, line_text)
                y -= line_height
                continue

            if row_render_mode is RowRenderMode.REPEAT:
                while x + token_width <= layout.right:
                    pdf.drawString(x, y, line_text)
                    x += token_width

                y -= line_height
                continue

            raise ValueError(f"Unsupported row render mode: {row_render_mode}")

        raise ValueError(f"Unsupported guide style: {guide_style}")


def _set_page_characteristics(pdf: Canvas, font_name: str, layout: PageLayout) -> Canvas:
    pdf.setFont(font_name, layout.text_font_size)
    # Text uses fill color; guide cells set their own stroke colors/styles.
    pdf.setFillColor(colors.HexColor(layout.text_fill_color))
    return pdf

def _start_new_page(pdf: Canvas, font_name: str, layout: PageLayout) -> Canvas:
    # start the new page
    pdf.showPage()
    # reset defaults
    pdf = _set_page_characteristics(pdf, font_name, layout)
    return pdf


def _draw_dotted_plus_cell(
        pdf,
        x: float,
        y_baseline: float,
        cell_w: float,
        cell_h: float,
        layout: PageLayout,
) -> None:
    """
    Draw one guide cell with a solid border and dashed center "+" guide.

    Args:
        pdf: ReportLab canvas object used for drawing.
        x: Left edge of the guide cell.
        y_baseline: Text baseline used to anchor vertical placement.
        cell_w: Guide cell width.
        cell_h: Guide cell height.
        layout: Page layout providing guide style and geometry policy.
    """
    # Place the box relative to the baseline using layout policy.
    y_bottom = y_baseline - layout.guide_baseline_offset

    # Preserve current stroke style so changes stay local to this helper.
    previous_line_width = pdf._lineWidth
    previous_stroke_color = pdf._strokeColorObj

    # Apply configured guide stroke width.
    pdf.setLineWidth(layout.guide_line_width)

    # Solid outer border.
    pdf.setStrokeColor(colors.HexColor(layout.guide_border_color))
    pdf.setDash()
    pdf.rect(x, y_bottom, cell_w, cell_h, stroke=1, fill=0)

    # Dashed center "+" lines.
    pdf.setStrokeColor(colors.HexColor(layout.guide_center_color))
    pdf.setDash(layout.guide_dash_on, layout.guide_dash_off)
    pdf.line(x + cell_w / 2, y_bottom, x + cell_w / 2, y_bottom + cell_h)
    pdf.line(x, y_bottom + cell_h / 2, x + cell_w, y_bottom + cell_h / 2)

    # Restore previous stroke state.
    pdf.setDash()
    pdf.setStrokeColor(previous_stroke_color)
    pdf.setLineWidth(previous_line_width)
