"""Tests de la línea de comandos: llaman a main() con argumentos simulados."""

import pytest

from scaffold import __version__
from scaffold.cli import main


def test_version_prints_version(capsys):
    with pytest.raises(SystemExit) as exit_info:
        main(["--version"])

    assert exit_info.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_no_command_shows_help(capsys):
    assert main([]) == 0
    assert "usage: scaffold" in capsys.readouterr().out


def test_new_creates_project_in_current_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    assert main(["new", "mi-api"]) == 0
    assert (tmp_path / "mi-api" / "README.md").is_file()


def test_new_returns_error_if_folder_exists(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "mi-api").mkdir()

    assert main(["new", "mi-api"]) == 1
    assert "ya existe" in capsys.readouterr().err


def test_new_returns_error_with_unknown_template(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    assert main(["new", "mi-api", "-t", "rust"]) == 1
    assert "no existe" in capsys.readouterr().err
