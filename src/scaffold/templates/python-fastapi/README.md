# $project_name

API REST con FastAPI. Proyecto creado en $year con scaffold.

## Requisitos

- Python 3.11 o superior

## Puesta en marcha

```bash
python -m venv .venv
python -m pip install -e . --group dev
python -m uvicorn $package_name.main:app --reload
```

Abre http://127.0.0.1:8000/health o la documentación automática en http://127.0.0.1:8000/docs.

## Tests

```bash
python -m pytest
```
