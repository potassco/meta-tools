"""
Base class for reification extensions.
Should be inherited by all extensions.
"""

from argparse import _ArgumentGroup
from typing import List

from clingo import Control
from clingo.ast import AST, parse_files, parse_string


class ReifyExtension:
    """Base class for reification extensions. Should be inherited by all extensions."""

    def register_options(self, parser: _ArgumentGroup) -> None:
        """
        Register the extensions's options to the parser for command line usage

        Arguments
        ---------
        parser: _ArgumentGroup
            Target argument group to register with.
        """

    def visit_ast(self, ast: AST) -> AST:  # nocoverage
        """
        Handle the given AST node and return the transformed AST node.
        Can be implemented using a transformer.
        """
        return ast

    def transform(self, file_paths: List[str], program_string: str) -> str:
        """
        Transforms a list of files and a program string and returns a string with the transformation

        Note: I have it as a general function so that it can use something other than a transformer, like ASPEN
        Note: Having it like this implies multiple passes over the program

        Args:
            file_paths (List[str]): The list of file paths to process.
            program_string (str): The program string to process.

        Returns:
            str: The transformed program string.
        """
        prg = ""

        def add_to_prg(ast: AST) -> None:
            nonlocal prg
            prg += str(self.visit_ast(ast)) + "\n"

        if len(file_paths) > 0:
            parse_files(file_paths, add_to_prg)

        if program_string is not None:
            parse_string(program_string, add_to_prg)

        return prg

    def add_extension_encoding(self, ctl: Control) -> None:
        """
        Add the extension's encoding to the given control object.
        This control object is used to obtain the reification
        Arguments
        ---------
        ctl
            Target control object.
        """
