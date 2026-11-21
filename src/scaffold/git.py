"""Inicializa un repositorio git en un proyecto generado.

Ejecuta el programa `git` del sistema con subprocess. No imprime nada:
los errores se comunican con GitError y la CLI decide cómo mostrarlos.
"""

import subprocess
from pathlib import Path

GIT_EXECUTABLE = "git"
INITIAL_BRANCH = "main"


class GitError(Exception):
    """Algo falló al ejecutar git."""


def init_repo(path: Path, message: str = "Commit inicial generado con scaffold") -> None:
    """Hace `git init`, `git add .` y el primer commit dentro de `path`."""
    _run(["init", "-b", INITIAL_BRANCH], cwd=path)
    _run(["add", "."], cwd=path)
    _run(["commit", "-m", message], cwd=path)


def _run(args: list[str], cwd: Path) -> None:
    """Ejecuta `git <args>` en `cwd` y traduce los fallos a GitError."""
    try:
        subprocess.run(
            [GIT_EXECUTABLE, *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True,
        )
    except FileNotFoundError:
        raise GitError("git no está instalado o no está en el PATH") from None
    except subprocess.CalledProcessError as error:
        detail = error.stderr.strip() or error.stdout.strip()
        if "user.name" in detail or "user.email" in detail:
            detail = (
                "git no sabe quién eres. Configúralo con:\n"
                '  git config --global user.name "Tu Nombre"\n'
                '  git config --global user.email "tu@email.com"'
            )
        raise GitError(f"falló 'git {args[0]}': {detail}") from None
