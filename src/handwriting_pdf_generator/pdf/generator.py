# high-level orchestration to create a PDF
from .pagenation import paginate_lines, plan_rows
from ..domain.worksheet_preset import WorksheetPreset, RowRenderMode, OutputLayoutMode

from .document import DEFAULT_OUTPUT_PATH, build_output_pdf_path, create_canvas
from .fonts import register_font
from .layout import build_single_page_layout, PageOrientation
from .renderer import (
    draw_title,
    draw_lines,
    set_page_characteristics
)


class Generator:

    def __init__(
            self,
            preset: WorksheetPreset,
            output_path: str = DEFAULT_OUTPUT_PATH,
            row_render_mode: RowRenderMode = RowRenderMode.REPEAT,
            page_orientation: PageOrientation = PageOrientation.LANDSCAPE,
            output_mode: OutputLayoutMode = OutputLayoutMode.BOOKLET
    ):
        self.preset = preset
        self.output_path = output_path
        self.row_render_mode = row_render_mode
        self.page_orientation = page_orientation
        self.output_mode = output_mode

    def generate(self):
        output_path = build_output_pdf_path(self.output_path, self.preset.display_name)
        # TODO: allow user to choose font
        chosen_font = self.preset.available_fonts[0]
        font_name = register_font(chosen_font)

        layout = build_single_page_layout(page_orientation=self.page_orientation)
        pdf = create_canvas(output_path, title=self.preset.display_name, layout=layout)

        # break up prompts into lines which fit the printable area - not yet implemented
        lines = plan_rows(
            preset=self.preset,
        )
        # divide up content into logical pages
        logical_worksheet_pages = paginate_lines(preset=self.preset, layout=layout, lines=lines)

        # set the initial page characteristics
        set_page_characteristics(pdf, font_name, layout)

        # draw per page
        for page in logical_worksheet_pages:
            if page.title != "":
                draw_title(pdf, page.title, layout)

            draw_lines(
                pdf,
                page.lines,
                layout,
                font_name,
                self.row_render_mode,
                self.preset.guide_style
            )

            pdf.showPage()
            set_page_characteristics(pdf, font_name, layout)

        pdf.save()
