"""
Command-line entry point for the handwriting PDF generator package.

This module uses the Typer library to create a command-line interface (CLI) for generating handwriting PDFs.
It imports the main application instance and runs it when executed as a script.
Kept separately from the cli directory to make it easier to switch out later with an interface.
"""

from .cli.app import app

if __name__ == "__main__":
    app()