"""Lógica para generar proyectos. No sabe nada de argparse ni de la terminal."""

import re
import tomllib
from dataclasses import dataclass
from datetime import date
from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path
from string import Template

TEMPLATES = files("scaffold") / "templates"
METADATA_FILE = "template.toml"
DEFAULT_TEMPLATE = "python"
_VALID_NAME = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")


@dataclass(frozen=True)
class TemplateInfo:
    """Datos que describen una plantilla (leídos de su template.toml)."""

    name: str
    description: str
    language: str


def available_templates() -> list[str]:
    """Devuelve los nombres de las plantillas disponibles."""
    return sorted(item.name for item in TEMPLATES.iterdir() if item.is_dir())


def template_info(name: str) -> TemplateInfo:
    """Lee el template.toml de la plantilla `name`."""
    text = (TEMPLATES / name / METADATA_FILE).read_text(encoding="utf-8")
    data = tomllib.loads(text)
    return TemplateInfo(name=name, description=data["description"], language=data["language"])


def list_templates() -> list[TemplateInfo]:
    """Devuelve la información de todas las plantillas, ordenadas por nombre."""
    return [template_info(name) for name in available_templates()]


def validate_name(name: str) -> str | None:
    """Devuelve un mensaje de error si `name` no vale como nombre de proyecto, o None."""
    if not name:
        return "el nombre no puede estar vacío"
    if not _VALID_NAME.fullmatch(name):
        return "usa solo letras, números, '-' y '_', empezando por una letra"
    return None


def build_variables(name: str) -> dict[str, str]:
    """Calcula los valores que se sustituyen en las plantillas."""
    return {
        "project_name": name,
        "package_name": name.replace("-", "_").lower(),
        "year": str(date.today().year),
    }


@dataclass(frozen=True)
class PlannedFile:
    """Un archivo que se va a crear: ruta relativa al proyecto y contenido final."""

    path: Path
    content: str


def plan(name: str, template: str) -> list[PlannedFile]:
    """Calcula qué archivos tendría el proyecto, SIN tocar el disco.

    Lanza ValueError si la plantilla no existe.
    """
    if template not in available_templates():
        options = ", ".join(available_templates())
        raise ValueError(f"la plantilla '{template}' no existe (disponibles: {options})")

    variables = build_variables(name)
    files: list[PlannedFile] = []
    _collect(TEMPLATES / template, Path(), variables, files)
    return sorted(files, key=lambda f: f.path.as_posix())


def write(files: list[PlannedFile], destination: Path) -> None:
    """Escribe en `destination` los archivos de un plan.

    Lanza FileExistsError si la carpeta destino ya existe.
    """
    if destination.exists():
        raise FileExistsError(f"la carpeta '{destination}' ya existe")
    for file in files:
        target = destination / file.path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(file.content, encoding="utf-8")


def generate(name: str, template: str, destination: Path) -> None:
    """Crea el proyecto `name` en `destination` usando la plantilla `template`.

    Lanza ValueError si la plantilla no existe y FileExistsError si la
    carpeta destino ya existe.
    """
    write(plan(name, template), destination)


def _collect(
    source: Traversable,
    relative: Path,
    variables: dict[str, str],
    files: list[PlannedFile],
) -> None:
    """Recorre `source` recursivamente y añade a `files` cada archivo ya
    sustituido (nombre y contenido). `relative` es la ruta dentro del proyecto."""
    for item in source.iterdir():
        if item.name == METADATA_FILE:
            continue  # los metadatos describen la plantilla, no forman parte del proyecto
        target = relative / Template(item.name).safe_substitute(variables)
        if item.is_dir():
            _collect(item, target, variables, files)
        else:
            content = item.read_text(encoding="utf-8")
            files.append(PlannedFile(target, Template(content).safe_substitute(variables)))
