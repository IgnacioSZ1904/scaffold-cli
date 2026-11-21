"""Modo consola: un prompt `scaffold>` donde escribir comandos uno tras otro.

Se abre al ejecutar `scaffold` sin argumentos en una terminal, por ejemplo al
hacer doble clic en el .exe. Cada línea se procesa igual que si se hubiera
escrito en la terminal: se trocea con shlex y se pasa a main().
"""

import shlex
from collections.abc import Callable
from contextlib import suppress

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter

from scaffold import ui

EXIT_WORDS = {"exit", "quit", "salir"}
COMMANDS = ["new", "list", "help", *sorted(EXIT_WORDS)]


def run_shell(run_command: Callable[[list[str]], int]) -> int:
    """Bucle de la consola. `run_command` es la función main del CLI.

    Se recibe como parámetro (en vez de importarla) para evitar un import
    circular: cli importa shell, así que shell no puede importar cli.
    """
    ui.show_banner()
    session = PromptSession(completer=WordCompleter(COMMANDS))

    while True:
        try:
            line = session.prompt("scaffold> ")
        except KeyboardInterrupt:  # Ctrl+C: descarta la línea y sigue
            continue
        except EOFError:  # Ctrl+D / Ctrl+Z: sale
            break

        args = parse_line(line)
        if args is None:
            continue
        if args[0] in EXIT_WORDS:
            break
        if args[0] == "help":
            args = ["--help"]

        # argparse llama a sys.exit() con --help o con argumentos erróneos;
        # en la consola eso no debe cerrar el programa.
        with suppress(SystemExit):
            run_command(args)

    ui.console.print("¡Hasta luego!", style="dim")
    return 0


def parse_line(line: str) -> list[str] | None:
    """Convierte una línea en lista de argumentos. Devuelve None si no hay nada útil."""
    try:
        args = shlex.split(line, posix=True)
    except ValueError as error:  # p. ej. comillas sin cerrar
        ui.error(f"no se pudo leer el comando: {error}")
        return None
    if args and args[0] == "scaffold":  # permite escribir "scaffold new ..." por costumbre
        args = args[1:]
    return args or None
