# high-level orchestration to create a PDF
from .booklet import impose_booklet_pages
from .pagenation import (
    paginate_lines,
    plan_rows
)
from ..domain.worksheet_preset import (
    WorksheetPreset,
    RowRenderMode,
    OutputLayoutMode
)

from .document import (
    DEFAULT_OUTPUT_PATH,
    build_output_pdf_path,
    create_canvas
)
from .fonts import register_font
from .layout import (
    build_single_page_layout,
    PageOrientation,
    FontSize,
    build_booklet_page_one_layout
)
from .renderer import (
    draw_title,
    draw_lines_row_render_single,
    draw_lines_row_render_repeat,
    set_page_characteristics
)


class Generator:

    def __init__(
            self,
            preset: WorksheetPreset,
            output_path: str = DEFAULT_OUTPUT_PATH,
            row_render_mode: RowRenderMode = RowRenderMode.REPEAT,
            page_orientation: PageOrientation = PageOrientation.LANDSCAPE,
            output_mode: OutputLayoutMode = OutputLayoutMode.BOOKLET,
            font_size: FontSize = FontSize.FOURTEEN
    ):
        self.preset = preset
        self.output_path = output_path
        self.row_render_mode = row_render_mode
        self.page_orientation = page_orientation
        self.output_mode = output_mode
        self.font_size = font_size

    def generate(self):
        output_path = build_output_pdf_path(self.output_path, self.preset.display_name)
        # TODO: allow user to choose font
        chosen_font = self.preset.available_fonts[0]
        font_name = register_font(chosen_font)

        layout = build_single_page_layout(page_orientation=self.page_orientation, font_size=self.font_size)
        pdf = create_canvas(output_path, title=self.preset.display_name, layout=layout)

        # break up prompts into lines which fit the printable area - not yet implemented
        lines = plan_rows(
            preset=self.preset,
        )

        # divide up content into logical pages
        logical_worksheet_pages = paginate_lines(preset=self.preset, layout=layout, lines=lines)

        # organize pages into booklet order
        if self.output_mode is OutputLayoutMode.BOOKLET:
            logical_worksheet_pages = impose_booklet_pages(logical_worksheet_pages)

        # set the initial page characteristics
        set_page_characteristics(pdf, font_name, layout)

        if self.output_mode is OutputLayoutMode.SINGLE_PAGE:
            # draw per page
            self.draw_worksheet_single_page(font_name, layout, logical_worksheet_pages, pdf)
        elif self.output_mode is OutputLayoutMode.BOOKLET:
            self.draw_worksheet_booklet(font_name, layout, logical_worksheet_pages, pdf)

        pdf.save()


    def draw_worksheet_single_page(self, font_name, layout, logical_worksheet_pages, pdf):
        for i, page in enumerate(logical_worksheet_pages):
            if page is not None:

                if i > 0:
                    pdf.showPage()
                    set_page_characteristics(pdf, font_name, layout)

                if page.title != "":
                    draw_title(pdf, page.title, layout)

                # if single row mode is selected, reorganize the prompts to print as many as possible on a single line
                if self.row_render_mode is RowRenderMode.SINGLE:
                    draw_lines_row_render_single(
                        pdf,
                        page.lines,
                        layout,
                        font_name,
                        self.preset.guide_style
                    )
                elif self.row_render_mode is RowRenderMode.REPEAT:
                    draw_lines_row_render_repeat(
                        pdf,
                        page.lines,
                        layout,
                        font_name,
                        self.preset.guide_style
                    )
                else:
                    raise NotImplementedError(f"Unsupported row_render_mode: {self.row_render_mode}")


    def draw_worksheet_booklet(self, font_name, layout, logical_worksheet_pages, pdf):

        booklet_page_layout = build_booklet_page_one_layout(initial_layout=layout)

        for i, page in enumerate(logical_worksheet_pages):
            if page is not None:
                if i > 0 and (i % 2 == 0):
                    pdf.showPage()
                    set_page_characteristics(pdf, font_name, layout)

                if i % 2 == 0:
                    pdf.saveState()
                    full_width, _ = layout.page_size
                    half_width = full_width / 2
                    pdf.translate(half_width, 0)

                if page.title != "":
                    draw_title(pdf, page.title, booklet_page_layout)

                # if single row mode is selected, reorganize the prompts to print as many as possible on a single line
                if self.row_render_mode is RowRenderMode.SINGLE:
                    draw_lines_row_render_single(
                        pdf,
                        page.lines,
                        booklet_page_layout,
                        font_name,
                        self.preset.guide_style
                    )
                elif self.row_render_mode is RowRenderMode.REPEAT:
                    draw_lines_row_render_repeat(
                        pdf,
                        page.lines,
                        booklet_page_layout,
                        font_name,
                        self.preset.guide_style
                    )
                else:
                    raise NotImplementedError(f"Unsupported row_render_mode: {self.row_render_mode}")

                if i % 2 == 0:
                    pdf.restoreState()
