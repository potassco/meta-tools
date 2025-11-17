"""
Test cases for main application functionality.
"""

from unittest import TestCase

from meta_tools.extensions.tag.tag_extension import TagExtension


class TestTag(TestCase):
    """
    Test cases for main application functionality.
    """

    def test_tag_rule(self) -> None:
        """
        Test the tag transformer.
        """
        extender = TagExtension()
        input_program = """
        a :- b.
        % @mytag
        c.

        % @myconstraint(1)
        % @myconstraint2
        :- d, e.

        """
        expected_program = """
        a :- b; &tag_rule(rule_fo("a :- b.")) { }.
        c :- &tag_rule(rule_fo("c.")) { }; &tag_rule(mytag) { }.
        #false :- d; e; &tag_rule(rule_fo("#false :- d; e.")) { }; &tag_rule(myconstraint(1)) { }; &tag_rule(myconstraint2) { }.
        """
        expected_rules = expected_program.strip().splitlines()
        transformed_prg = extender.transform([], input_program)
        transformed_prg_rules = transformed_prg.strip().splitlines()
        for expected_rule in expected_rules:
            self.assertIn(expected_rule.strip(), transformed_prg_rules)

    def test_tag_atoms(self) -> None:
        """
        Test the tag transformer.
        """
        extender = TagExtension()
        input_program = """
        % Something else
        % @myatomtag :: a
        % @myatomtag :: a : b
        a :- b.
        % @mytag
        c.

        """
        expected_program = """
        % Something else
        #false :- not &tag_atom(myatomtag,a) { }; a.
        #false :- not &tag_atom(myatomtag,a) { }; a; b.
        a :- b; &tag_rule(rule_fo("a :- b.")) { }.
        c :- &tag_rule(rule_fo("c.")) { }; &tag_rule(mytag) { }.
        """
        expected_rules = expected_program.strip().splitlines()
        transformed_prg = extender.transform([], input_program)
        transformed_prg_rules = transformed_prg.strip().splitlines()
        for expected_rule in expected_rules:
            self.assertIn(expected_rule.strip(), transformed_prg_rules)

    def test_syntax_errors(self) -> None:
        """
        Test that syntax errors are handled gracefully.
        """
        extender = TagExtension()
        input_program = """
        % @mytag 1(something)
        a :- b
        """
        with self.assertRaises(Exception):
            extender.transform([], input_program)

        input_program = """
        % @atom_tag :: something with spaces
        """
        with self.assertRaises(Exception):
            extender.transform([], input_program)

        input_program = """
        % @atom_tag :: dot .
        a :- b
        """
        with self.assertRaises(Exception):
            extender.transform([], input_program)

        input_program = """
        % @atom_tag :: : a
        a :- b
        """
        with self.assertRaises(Exception):
            extender.transform([], input_program)
