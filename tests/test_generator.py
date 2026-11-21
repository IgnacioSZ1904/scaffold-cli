"""Tests de la lógica de generación (sin pasar por la línea de comandos)."""

import pytest

from scaffold import generator


def test_python_template_is_available():
    assert "python" in generator.available_templates()


def test_build_variables_converts_dashes_to_underscores():
    variables = generator.build_variables("mi-api")

    assert variables["project_name"] == "mi-api"
    assert variables["package_name"] == "mi_api"
    assert variables["year"].isdigit()


def test_generate_creates_expected_files(tmp_path):
    destination = tmp_path / "mi-api"

    generator.generate("mi-api", "python", destination)

    assert (destination / "README.md").is_file()
    assert (destination / "pyproject.toml").is_file()
    assert (destination / ".gitignore").is_file()
    assert (destination / "src" / "mi_api" / "__init__.py").is_file()


def test_generate_substitutes_variables_in_content(tmp_path):
    destination = tmp_path / "mi-api"

    generator.generate("mi-api", "python", destination)

    assert "# mi-api" in (destination / "README.md").read_text(encoding="utf-8")
    assert 'name = "mi-api"' in (destination / "pyproject.toml").read_text(encoding="utf-8")


def test_generate_leaves_no_unsubstituted_variables(tmp_path):
    """Detecta variables mal escritas en las plantillas (safe_substitute no falla)."""
    destination = tmp_path / "mi-api"

    generator.generate("mi-api", "python", destination)

    for path in destination.rglob("*"):
        assert "$" not in path.name, f"variable sin sustituir en el nombre: {path}"
        if path.is_file():
            assert "$" not in path.read_text(encoding="utf-8"), f"variable sin sustituir en: {path}"


def test_generate_fails_if_destination_exists(tmp_path):
    destination = tmp_path / "mi-api"
    destination.mkdir()

    with pytest.raises(FileExistsError):
        generator.generate("mi-api", "python", destination)


def test_generate_fails_with_unknown_template(tmp_path):
    destination = tmp_path / "mi-api"

    with pytest.raises(ValueError, match="no existe"):
        generator.generate("mi-api", "rust", destination)

    assert not destination.exists()
