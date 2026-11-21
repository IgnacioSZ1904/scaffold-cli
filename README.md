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

```bash
python -m scaffold --help
python -m scaffold new mi-proyecto
```
