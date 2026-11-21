"""Toda la salida por terminal del CLI.

Es el único módulo que sabe CÓMO se muestra la información (con Rich).
Los comandos solo dicen QUÉ mostrar: ui.error(...), ui.show_plan(...), etc.
"""

from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from scaffold.generator import PlannedFile, TemplateInfo

# Se crean una vez y se reutilizan. Rich escribe en sys.stdout / sys.stderr
# en el momento de imprimir, así que los tests pueden capturar la salida.
console = Console()
err_console = Console(stderr=True)

LANGUAGE_COLORS = {
    "Python": "yellow",
    "JavaScript": "bright_yellow",
    "TypeScript": "blue",
    "Java": "red",
    "C#": "magenta",
    "Go": "cyan",
}


def error(message: str) -> None:
    """Muestra un error en rojo por stderr."""
    err_console.print(Text.assemble(("Error: ", "bold red"), message), soft_wrap=True)


def warning(message: str) -> None:
    """Muestra un aviso en amarillo por stderr."""
    err_console.print(Text.assemble(("Aviso: ", "bold yellow"), message), soft_wrap=True)


def success(message: str) -> None:
    """Muestra un mensaje de éxito en verde."""
    console.print(Text(message, style="green"), soft_wrap=True)


def show_templates(templates: list[TemplateInfo]) -> None:
    """Muestra las plantillas en una tabla."""
    table = Table(title="Plantillas disponibles", title_style="bold")
    table.add_column("Nombre", style="bold")
    table.add_column("Lenguaje")
    table.add_column("Descripción", style="dim")

    for t in templates:
        color = LANGUAGE_COLORS.get(t.language, "white")
        table.add_row(t.name, Text(t.language, style=color), t.description)

    console.print(table)
    console.print(
        "Usa: python -m scaffold new <nombre> -t <plantilla>", style="dim", highlight=False
    )


def show_plan(files: list[PlannedFile], destination: Path, with_git: bool) -> None:
    """Muestra como árbol de carpetas lo que se crearía (modo --dry-run)."""
    console.print(
        Text.assemble(("[dry-run] ", "bold cyan"), f"Se crearían {len(files)} archivos en:"),
        soft_wrap=True,
    )
    console.print(str(destination), style="bold", soft_wrap=True, highlight=False)

    tree = Tree(Text(destination.name + "/", style="bold blue"))
    branches: dict[Path, Tree] = {Path(): tree}
    for file in files:
        parent = Path()
        for part in file.path.parent.parts:
            current = parent / part
            if current not in branches:
                branches[current] = branches[parent].add(Text(part + "/", style="bold blue"))
            parent = current
        branches[parent].add(file.path.name)
    console.print(tree)

    if with_git:
        console.print("Se inicializaría un repositorio git con un primer commit.", style="cyan")
    if destination.exists():
        warning(f"'{destination}' ya existe, la creación real fallaría.")


def show_summary(name: str, template: str, destination: Path, with_git: bool) -> None:
    """Muestra un panel final con el resultado y los siguientes pasos."""
    lines = Text()
    lines.append("Proyecto ", style="green")
    lines.append(name, style="bold green")
    lines.append(" creado con la plantilla ", style="green")
    lines.append(template, style="bold")
    lines.append(f"\n{destination}", style="dim")
    if with_git:
        lines.append("\nRepositorio git inicializado con un primer commit.", style="cyan")
    lines.append("\n\nSiguientes pasos:\n", style="bold")
    lines.append(f"  cd {name}\n")
    lines.append("  Lee el README.md para arrancarlo")

    console.print(Panel(lines, title="scaffold", border_style="green", expand=False))
