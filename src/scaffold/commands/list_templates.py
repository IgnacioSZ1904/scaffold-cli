"""Subcomando `list`: muestra las plantillas disponibles."""

import argparse

from scaffold import generator


def register(subparsers: argparse._SubParsersAction) -> None:
    """Añade el subcomando `list` al parser principal."""
    parser = subparsers.add_parser("list", help="muestra las plantillas disponibles")
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    """Imprime una tabla con nombre, lenguaje y descripción de cada plantilla."""
    templates = generator.list_templates()
    name_width = max(len(t.name) for t in templates)
    lang_width = max(len(t.language) for t in templates)

    for t in templates:
        print(f"{t.name:<{name_width}}  {t.language:<{lang_width}}  {t.description}")
    return 0
