"""Funciones para cargar datos."""

from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def load_csv(name: str, folder: str = "raw") -> pd.DataFrame:
    """Carga data/<folder>/<name> como DataFrame."""
    return pd.read_csv(DATA_DIR / folder / name)
