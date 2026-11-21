"""Subcomando `new`: crea un proyecto nuevo a partir de una plantilla."""

import argparse
import sys
from pathlib import Path

from scaffold import generator, git


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
    if args.output.is_file():
        print(f"Error: '{args.output}' es un archivo, no una carpeta", file=sys.stderr)
        return 1

    destination = (args.output / args.name).resolve()
    try:
        files = generator.plan(args.name, args.template)
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


def _print_plan(files: list[generator.PlannedFile], destination: Path) -> None:
    """Muestra el plan sin escribir nada."""
    print(f"[dry-run] Se crearían {len(files)} archivos en {destination}:")
    for file in files:
        print(f"  {file.path.as_posix()}")
    if destination.exists():
        print(f"[dry-run] Aviso: '{destination}' ya existe, la creación real fallaría.")
