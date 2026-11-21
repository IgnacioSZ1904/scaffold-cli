"""Subcomando `new`: crea un proyecto nuevo a partir de una plantilla."""

import argparse
import sys
from pathlib import Path

from scaffold import generator, git, prompts


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
        default=Path("."),
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
            print("Error: falta el nombre del proyecto", file=sys.stderr)
            return 2
        try:
            _ask_missing(args)
        except prompts.Cancelled:
            print("Cancelado.", file=sys.stderr)
            return 1

    error = generator.validate_name(args.name)
    if error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    template = args.template or generator.DEFAULT_TEMPLATE

    if args.output.is_file():
        print(f"Error: '{args.output}' es un archivo, no una carpeta", file=sys.stderr)
        return 1

    destination = (args.output / args.name).resolve()
    try:
        files = generator.plan(args.name, template)
        if args.dry_run:
            _print_plan(files, destination)
            if args.git:
                print("[dry-run] Se inicializaría un repositorio git con un primer commit.")
            return 0
        generator.write(files, destination)
    except (FileExistsError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(f"Proyecto '{args.name}' creado en {destination}")

    if args.git:
        try:
            git.init_repo(destination)
        except git.GitError as error:
            print(f"Aviso: el proyecto se creó, pero {error}", file=sys.stderr)
            return 1
        print("Repositorio git inicializado con un primer commit.")
    return 0


def _ask_missing(args: argparse.Namespace) -> None:
    """Modo interactivo: pregunta lo que no se pasó por la línea de comandos."""
    args.name = prompts.ask_name()
    if args.template is None:
        args.template = prompts.ask_template(
            generator.list_templates(), default=generator.DEFAULT_TEMPLATE
        )
    if not args.git:
        args.git = prompts.ask_git()


def _print_plan(files: list[generator.PlannedFile], destination: Path) -> None:
    """Muestra el plan sin escribir nada."""
    print(f"[dry-run] Se crearían {len(files)} archivos en {destination}:")
    for file in files:
        print(f"  {file.path.as_posix()}")
    if destination.exists():
        print(f"[dry-run] Aviso: '{destination}' ya existe, la creación real fallaría.")
