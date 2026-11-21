"""Tests de la integración con git (usan el git real del sistema)."""

import shutil
import subprocess

import pytest

from scaffold import git
from scaffold.cli import main

requires_git = pytest.mark.skipif(shutil.which("git") is None, reason="git no está instalado")


@pytest.fixture
def isolated_git(tmp_path, monkeypatch):
    """Aísla git de la configuración del usuario y le da una identidad de prueba.

    Así los tests funcionan igual en tu equipo y en la CI (donde no hay user.name).
    """
    empty_config = tmp_path / "gitconfig"
    empty_config.write_text("", encoding="utf-8")
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", str(empty_config))
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    for role in ("AUTHOR", "COMMITTER"):
        monkeypatch.setenv(f"GIT_{role}_NAME", "Test")
        monkeypatch.setenv(f"GIT_{role}_EMAIL", "test@example.com")


@requires_git
def test_init_repo_creates_repository_with_one_commit(tmp_path, isolated_git):
    (tmp_path / "README.md").write_text("hola", encoding="utf-8")

    git.init_repo(tmp_path)

    log = subprocess.run(
        ["git", "log", "--oneline"], cwd=tmp_path, capture_output=True, text=True, check=True
    )
    assert len(log.stdout.strip().splitlines()) == 1


@requires_git
def test_new_with_git_initializes_repository(tmp_path, monkeypatch, isolated_git, capsys):
    monkeypatch.chdir(tmp_path)

    assert main(["new", "mi-api", "--git"]) == 0
    assert (tmp_path / "mi-api" / ".git").is_dir()
    assert "git inicializado" in capsys.readouterr().out


def test_init_repo_without_git_raises_git_error(tmp_path, monkeypatch):
    monkeypatch.setattr(git, "GIT_EXECUTABLE", "git-que-no-existe")

    with pytest.raises(git.GitError, match="no está instalado"):
        git.init_repo(tmp_path)


def test_new_keeps_project_and_returns_1_if_git_fails(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(git, "GIT_EXECUTABLE", "git-que-no-existe")

    assert main(["new", "mi-api", "--git"]) == 1
    assert (tmp_path / "mi-api" / "README.md").is_file()
    assert "el proyecto se creó" in capsys.readouterr().err


def test_new_dry_run_with_git_creates_nothing(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)

    assert main(["new", "mi-api", "--dry-run", "--git"]) == 0
    assert "repositorio git" in capsys.readouterr().out
    assert list(tmp_path.iterdir()) == []
