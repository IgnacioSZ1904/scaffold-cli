"""Genera el ejecutable de scaffold con PyInstaller.

Uso (desde la raíz del repo):
    python -m pip install -e . --group build
    python scripts/build_exe.py

Resultado: dist/scaffold.exe en Windows (dist/scaffold en Linux/macOS).
"""

import os
from pathlib import Path

import PyInstaller.__main__

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = ROOT / "src" / "scaffold"

PyInstaller.__main__.run(
    [
        str(PACKAGE / "__main__.py"),  # script de entrada
        "--name=scaffold",  # nombre del ejecutable
        "--onefile",  # todo en un único archivo
        "--console",  # abre una ventana de consola
        "--clean",  # borra la caché de builds anteriores
        f"--paths={ROOT / 'src'}",  # dónde encontrar el paquete scaffold
        # Las plantillas no son código Python: hay que añadirlas a mano.
        # Formato ORIGEN{separador}DESTINO dentro del ejecutable.
        f"--add-data={PACKAGE / 'templates'}{os.pathsep}scaffold/templates",
        # Rich carga algunos módulos de forma dinámica; así PyInstaller los incluye.
        "--collect-submodules=rich",
        f"--distpath={ROOT / 'dist'}",
        f"--workpath={ROOT / 'build'}",
        f"--specpath={ROOT / 'build'}",
    ]
)
