"""Lógica para generar proyectos. No sabe nada de argparse ni de la terminal."""

from pathlib import Path


def generate(name: str, template: str, destination: Path) -> None:
    """Crea el proyecto `name` en `destination` usando la plantilla `template`.

    Lanza FileExistsError si la carpeta destino ya existe.
    """
    if destination.exists():
        raise FileExistsError(f"la carpeta '{destination}' ya existe")
    destination.mkdir(parents=True)
    # Próximo paso: copiar los archivos de la plantilla y sustituir variables.
