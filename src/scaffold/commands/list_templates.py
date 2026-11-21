"""Subcomando `list`: muestra las plantillas disponibles."""

import argparse

from scaffold import generator, ui


def register(subparsers: argparse._SubParsersAction) -> None:
    """Añade el subcomando `list` al parser principal."""
    parser = subparsers.add_parser("list", help="muestra las plantillas disponibles")
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    """Muestra una tabla con nombre, lenguaje y descripción de cada plantilla."""
    ui.show_templates(generator.list_templates())
    return 0
