"""Tests de la lógica de generación (sin pasar por la línea de comandos)."""

from string import Template

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


ALL_TEMPLATES = generator.available_templates()


def _template_files(template):
    """Recorre todos los archivos de una plantilla (dentro del paquete)."""
    pending = [generator.TEMPLATES / template]
    while pending:
        item = pending.pop()
        if item.is_dir():
            pending.extend(item.iterdir())
        else:
            yield item


@pytest.mark.parametrize("template", ALL_TEMPLATES)
def test_template_only_uses_known_variables(template):
    """Detecta variables mal escritas: substitute() (estricto) lanza KeyError.

    Un `$` literal en una plantilla debe escribirse como `$$`.
    """
    variables = generator.build_variables("mi-api")

    for item in _template_files(template):
        Template(item.name).substitute(variables)
        Template(item.read_text(encoding="utf-8")).substitute(variables)


@pytest.mark.parametrize("template", ALL_TEMPLATES)
def test_every_template_generates_readme_and_gitignore(tmp_path, template):
    destination = tmp_path / "mi-api"

    generator.generate("mi-api", template, destination)

    assert (destination / "README.md").is_file()
    assert (destination / ".gitignore").is_file()
    assert "# mi-api" in (destination / "README.md").read_text(encoding="utf-8")


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
