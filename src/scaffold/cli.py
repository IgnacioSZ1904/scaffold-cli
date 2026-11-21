"""Punto de entrada de la línea de comandos."""

import argparse

from scaffold import __version__
from scaffold.commands import list_templates, new


def build_parser() -> argparse.ArgumentParser:
    """Crea y devuelve el parser con todas las opciones del CLI."""
    parser = argparse.ArgumentParser(
        prog="scaffold",
        description="Genera el esqueleto de un proyecto con un solo comando.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    subparsers = parser.add_subparsers(title="comandos", dest="command")
    new.register(subparsers)
    list_templates.register(subparsers)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Lee los argumentos y ejecuta la orden. Devuelve el código de salida."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return 0
    return args.func(args)
