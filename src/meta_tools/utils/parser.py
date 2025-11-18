"""
The command line parser for the project.
"""

from argparse import ArgumentParser
from importlib import metadata
from typing import Any, Optional, cast

from rich.text import Text
from rich_argparse import ArgumentDefaultsRichHelpFormatter

from . import logging

__all__ = ["get_parser"]

VERSION = metadata.version("meta-tools-clingo")


ascii_art_reify = Text(
    r"""
          _  __
         (_)/ _|
 _ __ ___ _| |_ _   _
| '__/ _ \ |  _| | | |
| | |  __/ | | | |_| |
|_|  \___|_|_|  \__, |
                 __/ |
                |___/
    (Meta-Tools)
    """,
    no_wrap=True,
    justify="left",
)


def get_parser() -> ArgumentParser:
    """
    Return the parser for command line options.
    """
    parser = ArgumentParser(
        prog="reify",
        description=ascii_art_reify + "\n🚀 Reify CLI - Extended reification for meta programming.",  # type: ignore
        formatter_class=ArgumentDefaultsRichHelpFormatter,
    )
    levels = [
        ("error", logging.ERROR),
        ("warning", logging.WARNING),
        ("info", logging.INFO),
        ("debug", logging.DEBUG),
    ]

    def get(levels: list[tuple[str, int]], name: str) -> Optional[int]:
        for key, val in levels:
            if key == name:
                return val
        return None  # nocoverage

    parser.add_argument(
        "--log",
        default="warning",
        choices=[val for _, val in levels],
        metavar=f"{{{','.join(key for key, _ in levels)}}}",
        help="set log level [%(default)s]",
        type=cast(Any, lambda name: get(levels, name)),
    )

    parser.add_argument("files", nargs="+", metavar="FILE", help="Input file paths with .lp extension.")

    parser.add_argument(
        "-c",
        "--const",
        action="append",
        help="Replace term occurrences of <id> with <term> (must have form <id>=<term>)",
        type=lambda s: s if "=" in s else parser.error("Constants must have form <id>=<term>"),
    )

    parser.add_argument(
        "--view",
        action="store_true",
        default=False,
        help="Visualize reification using clingraph.",
    )

    parser.add_argument(
        "--clean",
        action="store_true",
        default=False,
        help="Clean the output by hiding non-essential atoms of the reification"
        "and auxiliary rules added by the extensions.",
    )

    parser.add_argument(
        "--classic",
        action="store_true",
        default=False,
        help="Use the classic reification from clingo without extensions.",
    )

    parser.add_argument(
        "--save-out",
        action="store_true",
        default=False,
        help="Save temporary files during the reification process. A directory 'out' will be created for this purpose.",
    )

    parser.add_argument("--version", "-v", action="version", version=f"%(prog)s {VERSION}")
    return parser
