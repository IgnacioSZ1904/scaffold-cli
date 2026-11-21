"""Subcomando `new`: crea un proyecto nuevo a partir de una plantilla."""

import argparse
import sys
from pathlib import Path

from scaffold import generator, git, prompts, ui


def register(subparsers: argparse._SubParsersAction) -> None:
    """Añade el subcomando `new` y sus argumentos al parser principal."""
    parser = subparsers.add_parser("new", help="crea un proyecto nuevo")
    parser.add_argument(
        "name",
        nargs="?",
        help="nombre del proyecto; si no se indica, se pregunta (modo interactivo)",
    )
    parser.add_argument(
        "--template",
        "-t",
        help=f"plantilla a usar (por defecto: {generator.DEFAULT_TEMPLATE})",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        help="carpeta donde crear el proyecto (por defecto: la carpeta actual)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="muestra qué archivos se crearían, sin crear nada",
    )
    parser.add_argument(
        "--git",
        action="store_true",
        help="inicializa un repositorio git y hace el primer commit",
    )
    parser.set_defaults(func=run)


def run(args: argparse.Namespace) -> int:
    """Traduce los argumentos a una llamada al generador."""
    if args.name is None:
        if not sys.stdin.isatty():
            ui.error("falta el nombre del proyecto")
            return 2
        try:
            _ask_missing(args)
        except prompts.Cancelled:
            ui.warning("cancelado por el usuario")
            return 1

    error = generator.validate_name(args.name)
    if error:
        ui.error(error)
        return 1
    template = args.template or generator.DEFAULT_TEMPLATE
    output = args.output or Path(".")

    if output.is_file():
        ui.error(f"'{output}' es un archivo, no una carpeta")
        return 1

    destination = (output / args.name).resolve()
    try:
        files = generator.plan(args.name, template)
        if args.dry_run:
            ui.show_plan(files, destination, with_git=args.git)
            return 0
        generator.write(files, destination)
    except (FileExistsError, ValueError) as error:
        ui.error(str(error))
        return 1

    if args.git:
        try:
            git.init_repo(destination)
        except git.GitError as error:
            ui.success(f"Proyecto '{args.name}' creado en {destination}")
            ui.warning(f"el proyecto se creó, pero {error}")
            return 1

    ui.show_summary(args.name, template, destination, with_git=args.git)
    return 0


def _ask_missing(args: argparse.Namespace) -> None:
    """Modo interactivo: pregunta lo que no se pasó por la línea de comandos."""
    args.name = prompts.ask_name()
    if args.template is None:
        args.template = prompts.ask_template(
            generator.list_templates(), default=generator.DEFAULT_TEMPLATE
        )
    if args.output is None:
        args.output = prompts.ask_output()
    if not args.git:
        args.git = prompts.ask_git()
