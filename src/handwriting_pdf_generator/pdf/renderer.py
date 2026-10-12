# draw glyphs, guides, styling
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib import colors
from reportlab.pdfgen.canvas import Canvas

from ..domain.worksheet_preset import RowRenderMode, GuideStyle
from ..pdf.layout import PageLayout


def draw_title(pdf, title: str, layout: PageLayout) -> None:
    """
    Draw the worksheet title at the configured title position.

    The title is placed at the left page margin (`layout.left`) and at a vertical
    position derived from the top boundary (`layout.top`) minus
    `layout.title_top_offset`.

    Args:
        pdf: ReportLab canvas object used for drawing.
        title: Text to render as the page title.
        layout: Page layout containing title coordinates and font settings.
    """

    title_x = layout.left
    title_y = layout.top - layout.title_top_offset

    # Save the current fill color
    previous_fill_color = pdf._fillColorObj

    # Set the title color and draw
    pdf.setFillColor(colors.HexColor(layout.title_color))
    pdf.drawString(title_x, title_y, title)

    # Restore the previous fill color
    pdf.setFillColor(previous_fill_color)


def draw_lines_row_render_repeat(
        pdf: Canvas,
        lines: list[str],
        layout: PageLayout,
        font_name: str,
        guide_style: GuideStyle,
) -> None:
    """
    Draw worksheet practice rows for the provided text lines.

    This renderer supports two orthogonal dimensions of behavior:
    - Guide style:
      - `GuideStyle.PLUS_DOTTED`: draw guide cells with center cross lines.
      - `GuideStyle.NONE`: draw plain text only.

    Args:
        pdf: ReportLab canvas object used for drawing.
        lines: Text lines to render, one row per repeated prompt.
        layout: Page layout containing text origin, boundaries, spacing, and style.
        font_name: Font name used for line text.
        guide_style: Controls whether and how guide cells are drawn.

    Raises:
        ValueError: If `row_render_mode` or `guide_style` is unsupported.
    """

    line_height = layout.line_height
    y = layout.first_row_baseline

    for row in lines:
        text, definition = _extract_text_and_definition(row)
        text = text.strip()
        definition = definition.strip()
        # render empty row if line empty
        if not text:
            y -= line_height
            continue

        # reset horizontal drawing position for each row
        x = layout.left

        if definition:
            y = _draw_definition_block(pdf, definition, y, font_name, layout)

        token_width = stringWidth(text, font_name, layout.text_font_size)

        if token_width <= 0:
            y -= line_height
            continue

        if guide_style is GuideStyle.PLUS_DOTTED:
            while x + layout.guide_cell_width <= layout.right:
                _draw_dotted_plus_cell(pdf, x, y, layout.guide_cell_width, layout.guide_cell_height, layout)
                text_x = x + (layout.guide_cell_width - token_width) / 2
                pdf.drawString(text_x, y, text)
                x += layout.guide_cell_step

        elif guide_style is GuideStyle.NONE:
            while x + token_width <= layout.right:
                pdf.drawString(x, y, text)
                x += token_width

        else:
            raise ValueError(f"Unsupported guide style: {guide_style}")

        y -= line_height


def draw_lines_row_render_single(
        pdf: Canvas,
        prompts: list[str],
        layout: PageLayout,
        font_name: str,
        guide_style: GuideStyle,
) -> None:
    """
    Draw worksheet practice rows for the provided text lines.

    This renderer supports two orthogonal dimensions of behavior:
    - Guide style:
      - `GuideStyle.PLUS_DOTTED`: draw guide cells with center cross lines.
      - `GuideStyle.NONE`: draw plain text only.

    Args:
        pdf: ReportLab canvas object used for drawing.
        prompts: Text lines to render, multiple per row.
        layout: Page layout containing text origin, boundaries, spacing, and style.
        font_name: Font name used for line text.
        guide_style: Controls whether and how guide cells are drawn.

    Raises:
        ValueError: If `row_render_mode` or `guide_style` is unsupported.
    """

    line_height = layout.line_height
    y = layout.first_row_baseline
    x = layout.left

    for row in prompts:
        text, definition = _extract_text_and_definition(row)
        text = text.strip()
        definition = definition.strip()

        # skip if not present
        if not text:
            continue

        if definition:
            x = layout.left
            y = _draw_definition_block(pdf, definition, y, font_name, layout)

        # keep track of token width to ensure there is something to draw
        # and we do not draw past the page margin
        token_width = stringWidth(text, font_name, layout.text_font_size)

        # skip to next prompt if token has no width
        if token_width <= 0:
            continue

        if guide_style is GuideStyle.PLUS_DOTTED:
            required_width = layout.guide_cell_width
            advance_width = layout.guide_cell_step

            # determine if the next cell will fit on the current line; if not, move to the next line
            if x + required_width > layout.right:
                x = layout.left
                y -= line_height

            # draw the grid cell with a dotted plus sign in the center
            _draw_dotted_plus_cell(pdf, x, y, layout.guide_cell_width, layout.guide_cell_height, layout)
            # determine the x-coordinate for the text inside the cell to ensure it stays centered
            text_x = x + (layout.guide_cell_width - token_width) / 2
            pdf.drawString(text_x, y, text)
            x += advance_width

        elif guide_style is GuideStyle.NONE:
            required_width = token_width

            # determine if prompt will fit on current line, otherwise move to next line
            if x + required_width > layout.right:
                x = layout.left
                y -= line_height

            pdf.drawString(x, y, text)
            x += token_width

        else:
            raise ValueError(f"Unsupported guide style: {guide_style}")


def set_page_characteristics(
        pdf: Canvas,
        font_name: str,
        layout: PageLayout
) -> None:
    """
    Set the page characteristics for the given PDF canvas:
    - font
    - fill (text) color

    :param pdf: the ReportLab canvas object to configure
    :param font_name: the font name to be used
    :param layout: the page layout to be used
    :return:
    """
    pdf.setFont(font_name, layout.text_font_size)
    # Text uses fill color; guide cells set their own stroke colors/styles.
    pdf.setFillColor(colors.HexColor(layout.text_fill_color))


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


def _extract_text_and_definition(row) -> tuple[str, str]:
    # Backward-compatible adapter
    if hasattr(row, "text"):
        text = row.text or ""
        definition = getattr(row, "definition", "") or ""
        return text, definition
    return str(row or ""), ""


def _definition_font_size(layout: PageLayout) -> int:
    return min(layout.text_font_size, 12)


def _wrap_text_to_width(text: str, font_name: str, font_size: int, max_width: float) -> list[str]:
    words = text.split()
    if not words:
        return []

    lines = []
    current = words[0]

    for word in words[1:]:
        candidate = f"{current} {word}"
        if stringWidth(candidate, font_name, font_size) <= max_width:
            current = candidate
        else:
            lines.append(current)
            current = word

    lines.append(current)
    return lines


def _definition_lines(definition: str, font_name: str, layout: PageLayout) -> list[str]:
    return _wrap_text_to_width(
        definition,
        font_name,
        _definition_font_size(layout),
        layout.right - layout.left,
    )


def _draw_definition_block(
        pdf: Canvas,
        definition: str,
        y: float,
        font_name: str,
        layout: PageLayout,
) -> float:
    lines = _definition_lines(definition, font_name, layout)
    if not lines:
        return y

    previous_fill = pdf._fillColorObj
    pdf.setFillColor(colors.HexColor(layout.definition_color))
    pdf.setFont(font_name, _definition_font_size(layout))

    for line in lines:
        pdf.drawString(layout.left, y, line)
        y -= layout.line_height

    pdf.setFont(font_name, layout.text_font_size)
    pdf.setFillColor(previous_fill)
    return y
