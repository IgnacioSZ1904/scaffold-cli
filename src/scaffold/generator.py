"""Lógica para generar proyectos. No sabe nada de argparse ni de la terminal."""

from datetime import date
from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path
from string import Template

TEMPLATES = files("scaffold") / "templates"


def available_templates() -> list[str]:
    """Devuelve los nombres de las plantillas disponibles."""
    return sorted(item.name for item in TEMPLATES.iterdir() if item.is_dir())


def build_variables(name: str) -> dict[str, str]:
    """Calcula los valores que se sustituyen en las plantillas."""
    return {
        "project_name": name,
        "package_name": name.replace("-", "_").lower(),
        "year": str(date.today().year),
    }


def generate(name: str, template: str, destination: Path) -> None:
    """Crea el proyecto `name` en `destination` usando la plantilla `template`.

    Lanza ValueError si la plantilla no existe y FileExistsError si la
    carpeta destino ya existe.
    """
    if template not in available_templates():
        options = ", ".join(available_templates())
        raise ValueError(f"la plantilla '{template}' no existe (disponibles: {options})")
    if destination.exists():
        raise FileExistsError(f"la carpeta '{destination}' ya existe")

    variables = build_variables(name)
    destination.mkdir(parents=True)
    _copy_dir(TEMPLATES / template, destination, variables)


def _copy_dir(source: Traversable, target: Path, variables: dict[str, str]) -> None:
    """Copia `source` en `target` recursivamente, sustituyendo variables
    tanto en los nombres como en el contenido de los archivos."""
    for item in source.iterdir():
        target_name = Template(item.name).safe_substitute(variables)
        target_path = target / target_name
        if item.is_dir():
            target_path.mkdir()
            _copy_dir(item, target_path, variables)
        else:
            content = item.read_text(encoding="utf-8")
            rendered = Template(content).safe_substitute(variables)
            target_path.write_text(rendered, encoding="utf-8")
