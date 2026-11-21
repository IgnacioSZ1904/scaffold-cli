"""Preguntas del modo interactivo.

Es el único módulo que sabe CÓMO se pregunta (con questionary). El resto del
código solo recibe las respuestas, así que cambiar de librería solo toca aquí.
"""

from pathlib import Path

import questionary

from scaffold import generator


class Cancelled(Exception):
    """El usuario canceló el modo interactivo (Ctrl+C)."""


def _answer(question: questionary.Question):
    """Lanza la pregunta. questionary devuelve None si el usuario pulsa Ctrl+C."""
    answer = question.ask()
    if answer is None:
        raise Cancelled
    return answer


def ask_name() -> str:
    """Pide el nombre del proyecto y no deja continuar hasta que sea válido."""

    def validate(text: str) -> bool | str:
        error = generator.validate_name(text)
        return True if error is None else error

    return _answer(questionary.text("Nombre del proyecto:", validate=validate))


def ask_template(templates: list[generator.TemplateInfo], default: str) -> str:
    """Muestra las plantillas en una lista que se recorre con las flechas."""
    choices = [
        questionary.Choice(
            title=f"{t.name:<16} {t.language}",
            value=t.name,
            description=t.description,
        )
        for t in templates
    ]
    return _answer(questionary.select("Plantilla:", choices=choices, default=default))


def ask_output() -> Path:
    """Pide la carpeta donde crear el proyecto (Tab autocompleta rutas)."""

    def validate(text: str) -> bool | str:
        return "es un archivo, no una carpeta" if Path(text).is_file() else True

    answer = _answer(
        questionary.path(
            "Carpeta donde crearlo:",
            default=".",
            only_directories=True,
            validate=validate,
        )
    )
    return Path(answer or ".")


def ask_git() -> bool:
    """Pregunta si se inicializa un repositorio git."""
    return _answer(questionary.confirm("¿Inicializar un repositorio git?", default=True))
