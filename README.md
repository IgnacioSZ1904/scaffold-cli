# scaffold-cli

Herramienta de línea de comandos que genera el esqueleto de un proyecto con una sola orden.

## Instalación (desarrollo)

```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
python -m pip install --upgrade pip   # --group requiere pip >= 25.1
python -m pip install -e . --group dev
```

## Tests

```bash
python -m pytest
```

## Uso

Sin argumentos se abre la consola de scaffold (`scaffold>`), donde puedes escribir `new`, `list`, `help` o `salir`.


```bash
python -m scaffold --help
python -m scaffold list
python -m scaffold new                # modo interactivo
python -m scaffold new mi-proyecto -t python-fastapi -o ..\proyectos --git
python -m scaffold new mi-proyecto --dry-run
```

## Ejecutable de Windows

```bash
python -m pip install -e . --group build
python scripts/build_exe.py
```

Genera `dist/scaffold.exe`. Al abrirlo con doble clic muestra la consola de scaffold.
No está firmado digitalmente: Windows puede mostrar un aviso de SmartScreen o bloquearlo.
