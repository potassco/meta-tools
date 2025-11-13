import logging
import re
import sys
from typing import Optional

from clingo import String, Control
from clingo import ast as _ast
from clingo.ast import parse_string
from importlib.resources import path

from meta_tools.extensions import ReifyExtension

log = logging.getLogger(__name__)

TAG_THEORY = """
#theory tag {
    constant { };
    &tag_rule/1:constant,any;
    &tag_atom/2:constant,any
}.
"""


class TagExtension(ReifyExtension):
    """Extension to show the reified program."""

    def __init__(self) -> None:
        super().__init__()
        self.transformer = TagTransformer()

    def visit_ast(self, ast: _ast.AST) -> _ast.AST:
        """ """
        new_ast = self.transformer.visit(ast)
        return new_ast

    def transform(self, file_paths: list[str], program_string: str) -> str:
        """ """
        new_prg = super().transform(file_paths, program_string)
        new_prg += TAG_THEORY + "\n"
        return new_prg

    def add_extension_encoding(self, ctl: Control) -> None:
        """ """
        with path("meta_tools.extensions.tag", "encoding.lp") as base_encoding:
            log.debug("Loading encoding: %s", base_encoding)
            ctl.load(str(base_encoding))


class TagTransformer(_ast.Transformer):
    """
    Transforms the rules by adding a theory atom &tag_rule(rule_type) to the body of each rule.
    The rule_type can be one of "rule", "fact", or "constraint". It is determined based on the structure of the rule.
    """

    def __init__(self) -> None:
        super().__init__()
        self._rule_tags = set([])
        self._atom_rules = set([])

    def _save_rule_tag(self, node: _ast.AST) -> None:
        """ """
        if node.ast_type == _ast.ASTType.Rule:
            literal = node.head
            if literal.atom.ast_type == _ast.ASTType.SymbolicAtom:
                self._rule_tags.add(literal.atom.symbol)

    def _save_atom_rule(self, node: _ast.AST) -> None:
        """ """
        if node.ast_type == _ast.ASTType.Rule:
            self._atom_rules.add(node)

    def _handle_comment(self, node: _ast.AST) -> Optional[str]:
        """ """

        regex_atom = r"^\s*%\s*@([^\n]+?)\s*::\s*(.*)$"
        match = re.match(regex_atom, node.value)
        head = None
        body = None

        def _save_head_body(node: _ast.AST) -> None:
            """ """
            if node.ast_type == _ast.ASTType.Rule:
                nonlocal head, body
                if node.head is None:
                    raise RuntimeError(
                        "Expected head in the rule for tagging atoms. The head is the atom to be tagged."
                    )
                head = node.head
                body = "".join([f", {b}" for b in node.body])

        if match:
            tag = match.group(1)
            arg_2_rule = match.group(2).replace(":", ":-") + "."
            try:
                parse_string(arg_2_rule, _save_head_body)
            except Exception as e:
                sys.stderr.write(
                    f"\033[91mError parsing tags, in the atom tag {node}, everything after `:` should be a rule without `.`\n\033[0m"
                )
                sys.stderr.write(f"\033[91mTried to parse an invalid rule: {arg_2_rule}\n\033[0m")
                raise e

            s = f":- not &tag_atom({tag},{head}), {head} {body}."
            try:
                parse_string(s, self._save_atom_rule)
            except Exception as e:
                sys.stderr.write(f"\033[91mError parsing tags. Perhaps an additional `.`\n\033[0m")
                sys.stderr.write(f"\033[91mTried to generate an invalid rule: {s}\n\033[0m")
                raise e
            return "atom"

        regex_rule = r"^\s*%\s*@([^\n]+?)\s*$"

        match = re.match(regex_rule, node.value)

        if match:
            arg1 = match.group(1)
            s = arg1 + "."
            try:
                parse_string(s, self._save_rule_tag)
            except Exception as e:
                log.error("Syntax error parsing the following tag -> %s", s)
                log.error("Tags for rules should be in the format: @tag_name")
                log.error("Tags for atoms should be in the format: @tag_name :: atom_to_tag : optional_conditions")
                raise RuntimeError(f"Error parsing tags {s}") from e
            return "rule"

        return None

    def _construct_theory_atom_literal(self, location, function):
        theory_tag = _ast.TheoryAtom(
            location=location,
            term=_ast.Function(location, "tag_rule", [function], 0),
            elements=[],
            guard=None,
        )
        body_literal = _ast.Literal(location=location, sign=_ast.Sign.NoSign, atom=theory_tag)
        return body_literal

    def _add_default_tag(self, node: _ast.AST) -> _ast.AST:
        """ """
        f = (
            _ast.Function(
                node.location,
                "rule_fo",
                [
                    _ast.SymbolicTerm(
                        node.location,
                        String(
                            string=str(node).replace('"', "'"),
                        ),
                    )
                ],
                0,
            ),
        )

        theory_tag_literal = self._construct_theory_atom_literal(node.location, f[0])

        node.body.insert(len(node.body), theory_tag_literal)

    def _add_saved_tags(self, node: _ast.AST) -> _ast.AST:
        """ """
        for fun in self._rule_tags:
            theory_tag_literal = self._construct_theory_atom_literal(
                node.location,
                fun,
            )

            node.body.insert(len(node.body), theory_tag_literal)

        self._rule_tags.clear()

    def visit_Comment(self, node: _ast.AST) -> _ast.AST:  # pylint: disable=C0103
        """ """
        comment_tag_type = self._handle_comment(node)

        if comment_tag_type == "atom" and len(self._atom_rules) > 0:
            return self._atom_rules.pop()
        return node

    def visit_Rule(self, node: _ast.AST) -> _ast.AST:  # pylint: disable=C0103
        """ """

        self._add_default_tag(node)
        self._add_saved_tags(node)

        final_node = node.update(**self.visit_children(node))
        return final_node
