"""
This module defines the command-line interface (CLI) for the Handwriting PDF Generator application
using the Typer library. It sets up the main application and registers the
default command for generating handwriting PDFs.
"""

import typer

# from src.handwriting_pdf_generator.cli.commands.generate import handwriting_pdf
from .commands.generate import handwriting_pdf

app = typer.Typer()
# Register the default command.
app.command(name="generate")(handwriting_pdf)