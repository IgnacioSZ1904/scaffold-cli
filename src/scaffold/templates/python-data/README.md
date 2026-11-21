# $project_name

Proyecto de análisis de datos. Creado en $year con scaffold.

## Estructura

- `data/raw/`: datos originales, nunca se modifican.
- `data/processed/`: datos limpios generados por el código.
- `notebooks/`: exploración con Jupyter.
- `src/$package_name/`: código reutilizable (carga, limpieza, gráficos).
- `tests/`: tests del código de `src/`.

## Puesta en marcha

```bash
python -m venv .venv
python -m pip install -e . --group dev
python -m jupyter lab
```

## Tests

```bash
python -m pytest
```
