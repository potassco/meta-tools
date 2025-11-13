import logging
from clingo import Control
from clingo import ast as _ast
from importlib.resources import path
from meta_tools.extensions import ReifyExtension

log = logging.getLogger(__name__)


class ShowExtension(ReifyExtension):
    """Extension to show the reified program."""

    def __init__(self) -> None:
        super().__init__()
        self.transformer = ShowTransformer()

    # def visit_ast(self, ast: _ast.AST) -> _ast.AST:
    #     """ """
    #     Should re-write show statements into rules
    #     new_ast = self.transformer.visit(ast)
    #     return new_ast

    def add_extension_encoding(self, ctl: Control) -> None:
        """ """
        with path("meta_tools.extensions.show", "encoding.lp") as base_encoding:
            log.debug("Loading encoding: %s", base_encoding)
            ctl.load(str(base_encoding))


class ShowTransformer(_ast.Transformer):
    """
    Transforms the rules by removing show statements and making them into extra rules.
    Its extension also adds a symbol table for the atoms.
    """

    pass
