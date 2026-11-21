"""Tests del modo interactivo.

No se prueba questionary (eso es cosa de la librería): se sustituyen las
funciones de prompts por respuestas fijas y se comprueba que la CLI las usa.
"""

import pytest

from scaffold import prompts
from scaffold.cli import main


@pytest.fixture
def terminal(monkeypatch):
    """Simula que el programa se ejecuta en una terminal real."""
    monkeypatch.setattr("sys.stdin.isatty", lambda: True)


def fake_answers(monkeypatch, name="mi-api", template="go", git=False):
    monkeypatch.setattr(prompts, "ask_name", lambda: name)
    monkeypatch.setattr(prompts, "ask_template", lambda templates, default: template)
    monkeypatch.setattr(prompts, "ask_git", lambda: git)


def test_without_name_asks_and_creates_project(tmp_path, monkeypatch, terminal):
    monkeypatch.chdir(tmp_path)
    fake_answers(monkeypatch, template="go")

    assert main(["new"]) == 0
    assert (tmp_path / "mi-api" / "go.mod").is_file()


def test_template_given_by_flag_is_not_asked(tmp_path, monkeypatch, terminal):
    monkeypatch.chdir(tmp_path)
    fake_answers(monkeypatch)

    def fail(*args, **kwargs):
        raise AssertionError("no debería preguntar la plantilla")

    monkeypatch.setattr(prompts, "ask_template", fail)

    assert main(["new", "-t", "python"]) == 0
    assert (tmp_path / "mi-api" / "pyproject.toml").is_file()


def test_cancel_returns_1_and_creates_nothing(tmp_path, monkeypatch, terminal, capsys):
    monkeypatch.chdir(tmp_path)

    def cancel():
        raise prompts.Cancelled

    monkeypatch.setattr(prompts, "ask_name", cancel)

    assert main(["new"]) == 1
    assert "cancelado" in capsys.readouterr().err
    assert list(tmp_path.iterdir()) == []


def test_without_name_and_without_terminal_fails(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin.isatty", lambda: False)

    assert main(["new"]) == 2
    assert "falta el nombre" in capsys.readouterr().err


def test_invalid_name_from_command_line_fails(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    assert main(["new", "mi api"]) == 1
    assert "letras" in capsys.readouterr().err
