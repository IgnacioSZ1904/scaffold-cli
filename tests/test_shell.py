"""Tests del modo consola (sin terminal real: se simulan las líneas escritas)."""

import pytest

from scaffold import shell


class FakeSession:
    """Sustituye a PromptSession: devuelve las líneas indicadas y luego Ctrl+D."""

    def __init__(self, lines):
        self.lines = list(lines)

    def prompt(self, message):
        if not self.lines:
            raise EOFError
        line = self.lines.pop(0)
        if isinstance(line, BaseException):
            raise line
        return line


@pytest.fixture
def run_with_lines(monkeypatch):
    """Ejecuta la consola con unas líneas y devuelve los comandos que recibió main()."""

    def _run(lines, command=None):
        received = []

        def fake_main(args):
            received.append(args)
            return command(args) if command else 0

        monkeypatch.setattr(shell, "PromptSession", lambda **kwargs: FakeSession(lines))
        assert shell.run_shell(fake_main) == 0
        return received

    return _run


def test_each_line_is_passed_to_main_as_arguments(run_with_lines):
    received = run_with_lines(["list", 'new "mi-api" -t go'])

    assert received == [["list"], ["new", "mi-api", "-t", "go"]]


def test_exit_words_close_the_shell(run_with_lines):
    received = run_with_lines(["salir", "list"])

    assert received == []


def test_help_and_scaffold_prefix_are_translated(run_with_lines):
    received = run_with_lines(["help", "scaffold list", ""])

    assert received == [["--help"], ["list"]]


def test_ctrl_c_does_not_close_the_shell(run_with_lines):
    received = run_with_lines([KeyboardInterrupt(), "list"])

    assert received == [["list"]]


def test_system_exit_from_argparse_does_not_close_the_shell(run_with_lines):
    def exits(args):
        raise SystemExit(2)

    received = run_with_lines(["new --opcion-rara", "list"], command=exits)

    assert len(received) == 2


def test_unclosed_quotes_show_error(capsys):
    assert shell.parse_line('new "mi-api') is None
    assert "no se pudo leer" in capsys.readouterr().err
