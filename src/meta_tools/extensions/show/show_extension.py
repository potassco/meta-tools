import logging
from importlib.resources import path
from typing import List

from clingo import Control
from clingo import ast as _ast

from meta_tools.extensions.base_extension import ReifyExtension

log = logging.getLogger(__name__)


class ShowExtension(ReifyExtension):
    """Extension to show the reified program."""

    def __init__(self) -> None:
        super().__init__()
        self.transformer = ShowTransformer()

    def visit_ast(self, ast: _ast.AST) -> _ast.AST:
        """ """
        log.debug("Visiting AST for show extension.")
        new_ast = self.transformer.visit(ast)
        return new_ast

    def add_extension_encoding(self, ctl: Control) -> None:
        """ """
        with path("meta_tools.extensions.show", "encoding.lp") as base_encoding:
            log.debug("Loading encoding: %s", base_encoding)
            ctl.load(str(base_encoding))

    def transform(self, file_paths: List[str], program_string: str) -> str:
        """
        Adds rules to hide all atoms not explicitly shown.
        """
        prg = super().transform(file_paths, program_string)
        if self.transformer.hide_all:
            prg += f"{self.transformer.show_fun_name}.\n"
        return prg


class ShowTransformer(_ast.Transformer):
    """
    Transforms the rules by removing show statements and making them into extra rules.
    Its extension also adds a symbol table for the atoms.
    """

    show_fun_name: str = "_show"

    def __init__(self) -> None:
        super().__init__()
        self.hide_all: bool = False

    def visit_ShowTerm(self, node: _ast.AST) -> _ast.AST:  # pylint: disable=C0103
        loc = node.location
        show_atom = _ast.Function(loc, self.show_fun_name, [_ast.SymbolicAtom(node.term)], False)
        head = _ast.Literal(loc, _ast.Sign.NoSign, show_atom)
        rule = _ast.Rule(loc, head, node.body)
        return rule

    def visit_ShowSignature(self, node: _ast.AST) -> _ast.AST:  # pylint: disable=C0103
        self.hide_all = True
        loc = node.location
        args = []
        for i in range(node.arity):
            args.append(_ast.Variable(loc, f"V{i}"))
        sig_as_atom = _ast.Function(loc, node.name, args, False)
        show_atom = _ast.Function(loc, self.show_fun_name, [sig_as_atom], False)
        head = _ast.Literal(loc, _ast.Sign.NoSign, show_atom)
        body = [_ast.Literal(loc, _ast.Sign.NoSign, sig_as_atom)]

        rule = _ast.Rule(loc, head, body)
        return rule
