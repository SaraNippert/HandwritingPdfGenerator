# high-level orchestration to create a PDF

from ..domain.worksheet_preset import WorksheetPreset, RowRenderMode

from .document import DEFAULT_OUTPUT_PATH, build_output_pdf_path, create_canvas
from .fonts import register_font
from .layout import build_single_page_layout
from .renderer import draw_title, draw_character_lines


class Generator:

    def __init__(
            self,
            preset: WorksheetPreset,
            output_path: str = DEFAULT_OUTPUT_PATH,
            row_render_mode: RowRenderMode = RowRenderMode.REPEAT
    ):
        self.preset = preset
        self.output_path = output_path
        self.row_render_mode = row_render_mode

    def generate(self):
        output_path = build_output_pdf_path(self.output_path, self.preset.display_name)
        font_name = register_font(self.preset.available_fonts[0])

        layout = build_single_page_layout()
        pdf = create_canvas(output_path, title=self.preset.display_name, layout=layout)

        draw_title(pdf, self.preset.display_name, layout, font_name)
        draw_character_lines(
            pdf,
            self.preset.characters,
            layout,
            font_name,
            self.row_render_mode,
            self.preset.guide_style
        )

        pdf.save()
