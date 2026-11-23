# scaffold

**ES** · Genera la estructura inicial de un proyecto, lista para programar, con un solo comando.
**EN** · Generate a ready-to-code project skeleton with one command.

[![tests](https://github.com/IgnacioSZ1904/scaffold-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/IgnacioSZ1904/scaffold-cli/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

![scaffold demo](docs/demo.gif)

[Español](#español) · [English](#english)

---

## Español

### Qué resuelve

Empezar un proyecto implica repetir siempre los mismos pasos: estructura de carpetas, archivo de dependencias, `.gitignore`, un primer test, un README y `git init`. `scaffold` lo hace todo con un comando para 9 stacks habituales, y el proyecto generado ya arranca y pasa sus propios tests.

```bash
scaffold new mi-api -t python-fastapi --git
```

### Funcionalidades

- **9 plantillas**: Python (básica, FastAPI y ciencia de datos), Node/Express, Go, Java/Spring Boot, C#/ASP.NET Core, React + Vite y Angular.
- **Modo interactivo**: `scaffold new` sin argumentos pregunta el nombre, la plantilla y la carpeta, y se elige con las flechas.
- **Consola propia**: `scaffold` sin argumentos abre un prompt `scaffold>` con historial y autocompletado con Tab.
- **`--dry-run`**: muestra el árbol de archivos que se crearía sin tocar el disco.
- **`--git`**: inicializa un repositorio en `main` y hace el primer commit.
- **Ejecutable de Windows**: un único `.exe` generado con PyInstaller.

### Stack y por qué

| Herramienta | Por qué |
|---|---|
| `argparse` | Es librería estándar; quería aprender los fundamentos de un CLI antes de usar un framework como Click o Typer |
| `string.Template` | Las plantillas son archivos reales con `$variables`, así que no hace falta un motor de plantillas |
| `rich` | Tablas, árboles y paneles en la terminal, que pasan a ASCII solos si la terminal no admite otros caracteres |
| `questionary` / `prompt_toolkit` | Preguntas interactivas y la consola propia |
| `pytest` + GitHub Actions | 76 tests en Linux y Windows, con Python 3.11 y 3.14 |
| `ruff` | Linter y formateador, obligatorios en la CI |
| `setuptools` + layout `src/` | Los tests se ejecutan contra el paquete instalado, lo que detecta pronto los errores de empaquetado |

### Cómo ejecutarlo

Requiere Python 3.11 o superior.

```bash
git clone https://github.com/IgnacioSZ1904/scaffold-cli.git
cd scaffold-cli
python -m venv .venv
.venv\Scripts\activate            # Windows (Linux/macOS: source .venv/bin/activate)
python -m pip install --upgrade pip   # --group necesita pip >= 25.1
python -m pip install -e . --group dev
```

Uso:

```bash
python -m scaffold                     # consola propia
python -m scaffold list                # plantillas disponibles
python -m scaffold new                 # modo interactivo
python -m scaffold new mi-api -t go -o ../proyectos --git
python -m scaffold new mi-api --dry-run
```

Desarrollo:

```bash
python -m pytest
python -m ruff check .
python -m ruff format .
```

Ejecutable de Windows (no está firmado digitalmente, así que SmartScreen o Smart App Control pueden bloquearlo):

```bash
python -m pip install -e . --group build
python scripts/build_exe.py            # -> dist/scaffold.exe
```

### Arquitectura

```
cli.py ──> commands/new.py ──> generator.py   plan() -> list[PlannedFile]  (pura, sin E/S)
       │                │                     write(files, destination)    (único punto que escribe)
       │                ├──> git.py           git init / add / commit con subprocess
       │                ├──> prompts.py       preguntas interactivas (questionary)
       │                └──> ui.py            toda la salida por terminal (rich)
       ├─> commands/list_templates.py
       └─> shell.py                           consola scaffold> (prompt_toolkit)

templates/<nombre>/    archivos reales + template.toml (descripción, lenguaje)
```

Cada capa sabe solo lo que necesita: `generator.py` nunca imprime, los comandos nunca importan `rich` ni `questionary` y añadir una plantilla es añadir una carpeta, sin tocar código.

### Decisiones técnicas y aprendizajes

- **Planificar y luego escribir.** Al principio el generador copiaba los archivos directamente. Para añadir `--dry-run` tenía dos opciones: un flag `dry_run` dentro del bucle de copia, o dividir la generación en `plan()` (devuelve datos) y `write()` (escribe en disco). Elegí dividirla. Ahora el mismo plan sirve para el árbol del dry-run, la escritura real y los tests, que ya no necesitan escribir archivos para comprobar el resultado.
- **Lógica separada de la CLI.** `generator.py` no sabe nada de argparse, así que se testea llamando directamente a sus funciones, y la CLI se testea llamando a `main([...])` con argumentos simulados.
- **Validación estricta de las plantillas.** El generador usa `safe_substitute` para que un `$` literal en una plantilla no lo rompa, pero eso ocultaría erratas como `$projet_name`. Un test parametrizado aplica `substitute()`, la versión estricta, a todos los archivos de cada plantilla, y así una errata hace fallar la CI. Los `$` literales se escriben como `$$`.
- **Las plantillas son datos del paquete.** No son código Python, así que se declaran en `pyproject.toml` (incluidos archivos ocultos como `.gitignore`), se leen con `importlib.resources` y se añaden explícitamente al build de PyInstaller.
- **Tests que también pasan en la CI.** Los tests de git pasaban en mi equipo, pero habrían fallado en la CI, donde git no tiene `user.name`. Ahora aíslan la configuración de git con variables de entorno.
- **Limitaciones de Windows.** Mi equipo bloquea los ejecutables sin firmar, lo que afectaba a `pip.exe` y al `.exe` generado. Por eso la documentación usa `python -m ...` en todos los comandos.

### Próximos pasos

- [ ] Publicar en PyPI con releases automáticos desde GitHub Actions
- [ ] Plantillas definidas por el usuario desde una carpeta local (p. ej. `~/.scaffold/templates`)
- [ ] Variable `--author` leída de `git config`

### Licencia

[MIT](LICENSE)

---

## English

### What it solves

Starting a project means repeating the same steps every time: folder layout, dependency file, `.gitignore`, a first test, a README, `git init`. `scaffold` does all of that in one command, for 9 common stacks, with a project that already runs and passes its own tests.

```bash
scaffold new my-api -t python-fastapi --git
```

### Features

- **9 templates**: Python (basic, FastAPI, data science), Node/Express, Go, Java/Spring Boot, C#/ASP.NET Core, React + Vite, Angular.
- **Interactive mode**: run `scaffold new` with no arguments and pick name, template and folder with arrow keys.
- **Built-in console**: `scaffold` with no arguments opens a `scaffold>` prompt with history and Tab completion.
- **`--dry-run`**: shows the file tree that would be created, without touching the disk.
- **`--git`**: initializes a repository on `main` and makes the first commit.
- **Windows executable**: a single `.exe` built with PyInstaller.

### Stack and why

| Tool | Why |
|---|---|
| `argparse` | Standard library; I wanted to learn CLI fundamentals before using a framework like Click/Typer |
| `string.Template` | Templates are real files with `$variables`, so no template engine dependency is needed |
| `rich` | Tables, trees and panels in the terminal, with automatic fallback to ASCII |
| `questionary` / `prompt_toolkit` | Interactive prompts and the built-in console |
| `pytest` + GitHub Actions | 76 tests on Linux and Windows, Python 3.11 and 3.14 |
| `ruff` | Linting and formatting, enforced in CI |
| `setuptools` + `src/` layout | Tests run against the installed package, which catches packaging errors early |

### Getting started

Requires Python 3.11+.

```bash
git clone https://github.com/IgnacioSZ1904/scaffold-cli.git
cd scaffold-cli
python -m venv .venv
.venv\Scripts\activate            # Windows (Linux/macOS: source .venv/bin/activate)
python -m pip install --upgrade pip   # --group needs pip >= 25.1
python -m pip install -e . --group dev
```

Usage:

```bash
python -m scaffold                     # built-in console
python -m scaffold list                # available templates
python -m scaffold new                 # interactive mode
python -m scaffold new my-api -t go -o ../projects --git
python -m scaffold new my-api --dry-run
```

Development:

```bash
python -m pytest
python -m ruff check .
python -m ruff format .
```

Windows executable (it is not code-signed, so SmartScreen or Smart App Control may block it):

```bash
python -m pip install -e . --group build
python scripts/build_exe.py            # -> dist/scaffold.exe
```

### Architecture

```
cli.py ──> commands/new.py ──> generator.py   plan() -> list[PlannedFile]  (pure, no I/O)
       │                │                     write(files, destination)    (only place that writes)
       │                ├──> git.py           git init / add / commit via subprocess
       │                ├──> prompts.py       interactive questions (questionary)
       │                └──> ui.py            all terminal output (rich)
       ├─> commands/list_templates.py
       └─> shell.py                           scaffold> console (prompt_toolkit)

templates/<name>/      real files + template.toml (description, language)
```

Each layer only knows what it needs to: `generator.py` never prints, the commands never import `rich` or `questionary`, and adding a template means adding a folder, with no code changes.

### Technical decisions and lessons learned

- **Plan, then write.** At first the generator copied files directly. To support `--dry-run` I had two options: add a `dry_run` flag inside the copy loop, or split generation into `plan()` (returns data) and `write()` (touches the disk). I chose the split. The same plan now feeds the dry-run tree, the real write and the tests, which no longer need to write files to check the output.
- **Logic separated from the CLI.** `generator.py` knows nothing about argparse, so it is tested by calling functions directly, and the CLI is tested by calling `main([...])` with fake arguments.
- **Strict validation of templates.** The generator uses `safe_substitute` so that a literal `$` in a template does not crash it, but that would hide typos like `$projet_name`. A parametrized test runs the strict `substitute()` over every template file, so a typo fails CI. Literal dollars are written as `$$`.
- **Templates are package data.** Templates are not Python code, so they are declared in `pyproject.toml` (including dotfiles like `.gitignore`), read with `importlib.resources` and added explicitly to the PyInstaller build.
- **Tests that also pass in CI.** The git tests passed on my machine but would have failed in CI, where git has no `user.name`. They now isolate git config with environment variables.
- **Windows constraints.** My machine blocks unsigned executables, which affected `pip.exe` and the generated `.exe`. The docs use `python -m ...` everywhere for that reason.

### Next steps

- [ ] Publish to PyPI with automated releases from GitHub Actions
- [ ] User-defined templates from a local folder (e.g. `~/.scaffold/templates`)
- [ ] `--author` variable read from `git config`

### License

[MIT](LICENSE)
