"""Punto de entrada de la API."""

from fastapi import FastAPI

app = FastAPI(title="$project_name")


@app.get("/health")
def health() -> dict[str, str]:
    """Comprueba que la API está en marcha."""
    return {"status": "ok"}
