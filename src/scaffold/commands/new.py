"""Subcomando `new`: crea un proyecto nuevo a partir de una plantilla."""

import argparse
import sys
from pathlib import Path

from scaffold import generator


def register(subparsers: argparse._SubParsersAction) -> None:
    """Añade el subcomando `new` y sus argumentos al parser principal."""
    parser = subparsers.add_parser("new", help="crea un proyecto nuevo")
    parser.add_argument("name", help="nombre del proyecto (y de su carpeta)")
    parser.add_argument(
        "--template",
        "-t",
        default="python",
        help="plantilla a usar (por defecto: python)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=Path("."),
        help="carpeta donde crear el proyecto (por defecto: la carpeta actual)",
    )
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    """Traduce los argumentos a una llamada al generador."""
    if args.output.is_file():
        print(f"Error: '{args.output}' es un archivo, no una carpeta", file=sys.stderr)
        return 1

    destination = (args.output / args.name).resolve()
    try:
        generator.generate(args.name, args.template, destination)
    except (FileExistsError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(f"Proyecto '{args.name}' creado en {destination}")
    return 0
