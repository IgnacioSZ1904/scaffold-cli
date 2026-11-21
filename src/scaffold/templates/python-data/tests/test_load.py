import pandas as pd

from $package_name import load


def test_load_csv_reads_file(tmp_path, monkeypatch):
    (tmp_path / "raw").mkdir()
    (tmp_path / "raw" / "ejemplo.csv").write_text("a,b\n1,2\n", encoding="utf-8")
    monkeypatch.setattr(load, "DATA_DIR", tmp_path)

    df = load.load_csv("ejemplo.csv")

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["a", "b"]
