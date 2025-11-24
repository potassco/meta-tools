"""
Test cases for main application functionality.
"""

import tempfile
from unittest import TestCase

from meta_tools import classic_reify, transform
from meta_tools.extensions.show.show_extension import ShowExtension
from meta_tools.extensions.tag.tag_extension import TAG_THEORY, TagExtension


class TestMain(TestCase):
    """
    Test cases for main application functionality.
    """

    def test_classic_reify(self) -> None:
        """
        Test classic reification.
        """
        input_program = "a(1). b(X):-a(X)."
        rsymbols = classic_reify(["--preserve-facts=symtab"], input_program)
        expected_symbols = {
            "tag(incremental)",
            "atom_tuple(0)",
            "atom_tuple(0,1)",
            "literal_tuple(0)",
            "rule(disjunction(0),normal(0))",
            "atom_tuple(1)",
            "atom_tuple(1,2)",
            "rule(disjunction(1),normal(0))",
            "literal_tuple(1)",
            "literal_tuple(1,1)",
            "output(a(1),1)",
            "literal_tuple(2)",
            "literal_tuple(2,2)",
            "output(b(1),2)",
        }
        actual_symbols = {str(s).rstrip(".") for s in rsymbols}
        self.assertSetEqual(actual_symbols, expected_symbols)

        rsymbols = classic_reify([], input_program)
        expected_symbols = {
            "tag(incremental)",
            "atom_tuple(0)",
            "atom_tuple(0,1)",
            "literal_tuple(0)",
            "rule(disjunction(0),normal(0))",
            "atom_tuple(1)",
            "atom_tuple(1,2)",
            "rule(disjunction(1),normal(0))",
            "output(a(1),0)",
            "output(b(1),0)",
        }
        actual_symbols = {str(s).rstrip(".") for s in rsymbols}
        print("Actual symbols:")
        print(actual_symbols)
        self.assertSetEqual(actual_symbols, expected_symbols)

    def test_transform(self) -> None:
        """
        Test the file transformer.
        """

        input_program = """
        % @mytag
        a(1).
        """
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".lp") as temp_file:
            temp_file.write(input_program)
            temp_file.flush()
            temp_file_path = temp_file.name
        extensions = [
            TagExtension(include_fo=False),
            ShowExtension(),
        ]
        transformed_program = transform([temp_file_path], extensions=extensions)
        self.assertIn(
            TAG_THEORY.replace("\n", "").replace(" ", ""), transformed_program.replace("\n", "").replace(" ", "")
        )

        expected_program = """
        a(1) :- &tag_rule(mytag) { }.
        """
        self.assertIn(
            expected_program.replace("\n", "").replace(" ", ""), transformed_program.replace("\n", "").replace(" ", "")
        )
