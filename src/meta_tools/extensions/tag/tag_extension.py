import logging
import re
import sys
from importlib.resources import path
from typing import Optional

from clingo import Control, Number, String
from clingo import ast as _ast
from clingo.ast import parse_string

from meta_tools.extensions.base_extension import ReifyExtension

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

    def __init__(
        self,
        include_fo: bool = True,
        include_loc: bool = False,
        include_program: bool = False,
        include_id: bool = False,
    ) -> None:
        """
        Initialize the Tag extension.
        Args:
            include_fo (bool): Whether to include first-order representation for each rule as a tag.
            include_loc (bool): Whether to include location information in the tags.
            include_program (bool): Whether to include the program information in the tags, such as base.
            include_id (bool): Whether to include unique rule IDs in the tags. This would be used for the first order representation.
        """
        super().__init__()
        self.transformer = TagTransformer(
            include_fo=include_fo, include_loc=include_loc, include_program=include_program, include_id=include_id
        )

    def visit_ast(self, ast: _ast.AST) -> _ast.AST:
        """
        Visit and transform the AST.
        Args:
            ast (_ast.AST): The abstract syntax tree to visit.
        Returns:
            _ast.AST: The transformed abstract syntax tree.
        """
        new_ast = self.transformer.visit(ast)
        return new_ast

    def transform(self, file_paths: list[str], program_string: str) -> str:
        """
        Transform the program string by adding the tag theory.
        Args:
            file_paths (list[str]): The list of file paths to process.
            program_string (str): The program string to process.
        Returns:
            str: The transformed program string with the tag theory appended.
        """
        new_prg = super().transform(file_paths, program_string)
        new_prg += TAG_THEORY + "\n"
        return new_prg

    def add_extension_encoding(self, ctl: Control) -> None:
        """
        Add the extension encoding to the clingo control. This extension creates the tag/2 predicate.
        Args:
            ctl (Control): The clingo control object.
        """
        with path("meta_tools.extensions.tag", "encoding.lp") as base_encoding:
            log.debug("Loading encoding: %s", base_encoding)
            ctl.load(str(base_encoding))


class TagTransformer(_ast.Transformer):
    """
    Transforms the rules by adding a theory atom &tag_rule(rule_type) to the body of each rule.
    The rule_type can be one of "rule", "fact", or "constraint". It is determined based on the structure of the rule.
    """

    def __init__(
        self,
        include_fo: bool = True,
        include_loc: bool = False,
        include_program: bool = False,
        include_id: bool = False,
    ) -> None:
        """
        Initialize the TagTransformer.
        Args:
            include_fo (bool): Whether to include first-order representation for each rule as a tag
            include_loc (bool): Whether to include location information in the tags.
            include_program (bool): Whether to include the program information in the tags, such as base.
            include_id (bool): Whether to include unique rule IDs in the tags. This would be used for the first order representation.
        """
        super().__init__()
        self._rule_tags: set[_ast.AST] = set([])
        self._atom_rules: set[_ast.AST] = set([])
        self._include_fo = include_fo
        self._include_loc = include_loc
        self._include_program = include_program
        self._include_id = include_id
        self._current_program: tuple[str, list[_ast.AST]] = ("base", [])  #
        self._rule_id_counter = 0

    def _save_rule_tag(self, node: _ast.AST) -> None:
        """
        Save the rule tag from the AST node to be added to the next rule
        Args:
            node (_ast.AST): The AST node to process.
        Returns:
            None
        """
        if node.ast_type == _ast.ASTType.Rule:
            literal = node.head
            if literal.atom.ast_type == _ast.ASTType.SymbolicAtom:
                self._rule_tags.add(literal.atom.symbol)

    def _save_atom_rule(self, node: _ast.AST) -> None:
        """
        Save the atom tagging rule to be added to the program
        Args:
            node (_ast.AST): The AST node to process.
        """
        if node.ast_type == _ast.ASTType.Rule:
            self._atom_rules.add(node)

    def _handle_comment(self, node: _ast.AST) -> Optional[str]:
        """
        Handle the comment node to extract tags for atoms or rules.
        Args:
            node (_ast.AST): The AST comment node to process.
        Returns:
            Optional[str]: "atom" if an atom tag was found, "rule" if a rule tag was found, None otherwise.
        """

        head = None
        body = None

        def _save_head_body(node: _ast.AST) -> None:
            """ """
            if node.ast_type == _ast.ASTType.Rule:
                nonlocal head, body
                head = node.head
                body = "".join([f", {b}" for b in node.body])

        regex_atom = r"^\s*%\s*@([^\n]+?)\s*::\s*(.*)$"
        match = re.match(regex_atom, node.value)
        if match:
            tag = match.group(1)
            arg_2_rule = match.group(2).replace(":", ":-") + "."
            try:
                parse_string(arg_2_rule, _save_head_body)
            except Exception as e:
                sys.stderr.write(
                    f"\033[91mError parsing tags, in the atom tag {node}, everything after `::` should have the form of a poll using : and without `.`\n\033[0m"
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

    def _construct_theory_atom_literal(self, location: _ast.Location, function: _ast.AST) -> _ast.AST:
        """
        Generate a theory atom literal for the given function.
        Args:
            location (_ast.Location): The location of the AST node.
            function (_ast.AST): The function to be used in the theory atom.
        Returns:
            _ast.AST: The constructed theory atom literal.
        """
        theory_tag = _ast.TheoryAtom(
            location=location,
            term=_ast.Function(location, "tag_rule", [function], 0),
            elements=[],
            guard=None,
        )
        body_literal = _ast.Literal(location=location, sign=_ast.Sign.NoSign, atom=theory_tag)
        return body_literal

    def _add_fo_tag(self, node: _ast.AST) -> None:
        """
        Add the first-order representation tag to the rule body.
        Args:
            node (_ast.AST): The AST rule node to process.
        """
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

    def _add_id(self, node: _ast.AST) -> None:
        """
        Add the unique ID tag to the rules a tag rule_id(id).
        Args:
            node (_ast.AST): The AST rule node to process.
        """
        self._rule_id_counter += 1
        f = (
            _ast.Function(
                node.location,
                "rule_id",
                [
                    _ast.SymbolicTerm(
                        node.location,
                        Number(
                            int(self._rule_id_counter),
                        ),
                    ),
                ],
                0,
            ),
        )
        theory_tag_literal = self._construct_theory_atom_literal(node.location, f[0])
        node.body.insert(len(node.body), theory_tag_literal)

    def _add_loc_tag(self, node: _ast.AST) -> None:
        """
        Add the tag with the location information of the rules a tag rule_loc(column, filename, line).
        Args:
            node (_ast.AST): The AST rule node to process.
        """
        l = node.location.begin
        f = (
            _ast.Function(
                node.location,
                "rule_loc",
                [
                    _ast.SymbolicTerm(
                        node.location,
                        Number(
                            int(l.column),
                        ),
                    ),
                    _ast.SymbolicTerm(
                        node.location,
                        String(
                            str(l.filename),
                        ),
                    ),
                    _ast.SymbolicTerm(
                        node.location,
                        Number(
                            int(l.line),
                        ),
                    ),
                ],
                0,
            ),
        )

        theory_tag_literal = self._construct_theory_atom_literal(node.location, f[0])
        node.body.insert(len(node.body), theory_tag_literal)

    def _add_program_tag(self, node: _ast.AST) -> None:
        """
        Add the program information tag to the rule body.
        Args:
            node (_ast.AST): The AST rule node to process.
        """
        f = (
            _ast.Function(
                node.location,
                "program",
                [
                    _ast.Function(node.location, self._current_program[0], self._current_program[1], False),
                ],
                0,
            ),
        )

        theory_tag_literal = self._construct_theory_atom_literal(node.location, f[0])

        node.body.insert(len(node.body), theory_tag_literal)

    def _add_saved_tags(self, node: _ast.AST) -> None:
        """
        Add saved tags to the rule body.
        Args:
            node (_ast.AST): The AST rule node to process.
        """
        for fun in sorted(list(self._rule_tags), key=lambda x: str(x)):
            theory_tag_literal = self._construct_theory_atom_literal(
                node.location,
                fun,
            )

            node.body.insert(len(node.body), theory_tag_literal)

        self._rule_tags.clear()

    def visit_Comment(self, node: _ast.AST) -> _ast.AST:  # pylint: disable=C0103
        """
        Handle comment nodes to extract tags.
        """
        comment_tag_type = self._handle_comment(node)

        if comment_tag_type == "atom" and len(self._atom_rules) > 0:
            return self._atom_rules.pop()
        return node

    def visit_Rule(self, node: _ast.AST) -> _ast.AST:  # pylint: disable=C0103
        """
        Handle rule nodes, it will add the saved tags and the FO tag if enabled.
        """
        if self._include_fo:
            self._add_fo_tag(node)
        if self._include_loc:
            self._add_loc_tag(node)
        if self._include_program:
            self._add_program_tag(node)
        if self._include_id:
            self._add_id(node)
        self._add_saved_tags(node)

        final_node = node.update(**self.visit_children(node))
        return final_node

    def visit_Program(self, node: _ast.AST) -> _ast.AST:  # pylint: disable=C0103
        """
        Handle program nodes to keep track of the current program name.
        """
        self._current_program = (node.name, node.parameters)
        return node
