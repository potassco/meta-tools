"""
Test cases for main application functionality.
"""

from unittest import TestCase

from meta_tools.extensions.show.show_extension import ShowExtension


class TestShow(TestCase):
    """
    Test cases for main application functionality.
    """

    def test_show_extension(self) -> None:
        """
        Test the show extension.
        """
        extender = ShowExtension()
        input_program = """
        a.
        #show a/0.
        """
        expected_program = """
        a.
        _show(a) :- a.
        _show.
        """
        expected_rules = expected_program.strip().splitlines()
        transformed_prg = extender.transform([], input_program)
        transformed_prg_rules = transformed_prg.strip().splitlines()
        for expected_rule in expected_rules:
            self.assertIn(expected_rule.strip(), transformed_prg_rules)

    def test_show_extension_term(self) -> None:
        """
        Test the show extension.
        """
        extender = ShowExtension()
        input_program = """
        a.
        #show b:a.
        """
        expected_program = """
        a.
        _show(b) :- a.
        """
        expected_rules = expected_program.strip().splitlines()
        transformed_prg = extender.transform([], input_program)
        transformed_prg_rules = transformed_prg.strip().splitlines()
        for expected_rule in expected_rules:
            self.assertIn(expected_rule.strip(), transformed_prg_rules)
        self.assertNotIn("_show.", transformed_prg_rules)

    def test_show_extension_vars(self) -> None:
        """
        Test the show extension.
        """
        extender = ShowExtension()
        input_program = """
        a(1,2).
        #show a/2.
        """
        expected_program = """
        a(1,2).
        _show(a(V0,V1)) :- a(V0,V1).
        _show.
        """
        expected_rules = expected_program.strip().splitlines()
        transformed_prg = extender.transform([], input_program)
        transformed_prg_rules = transformed_prg.strip().splitlines()
        for expected_rule in expected_rules:
            self.assertIn(expected_rule.strip(), transformed_prg_rules)
