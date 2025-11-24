"""
Test cases for main application functionality.
"""

import tempfile
from io import StringIO
from unittest import TestCase

from meta_tools import classic_reify, extend_reification, transform
from meta_tools.extensions.show.show_extension import ShowExtension
from meta_tools.extensions.tag.tag_extension import TagExtension
from meta_tools.utils import logging
from meta_tools.utils.logging import configure_logging, get_logger
from meta_tools.utils.parser import get_parser
from meta_tools.utils.theory import extend_with_theory_symbols


class TestMain(TestCase):
    """
    Test cases for main application functionality.
    """

    def test_logger(self) -> None:
        """
        Test the logger.
        """
        sio = StringIO()
        configure_logging(sio, logging.INFO, True)
        log = get_logger("main")
        log.info("test123")
        self.assertRegex(sio.getvalue(), "test123")

    def test_parser(self) -> None:
        """
        Test the parser.
        """
        parser = get_parser()
        ret = parser.parse_args(["examples/simple.lp", "--log", "info"])
        self.assertEqual(ret.log, logging.INFO)

    def test_main(self) -> None:
        """
        Test the main function.
        """
        input_program1 = """
        % @mytag
        a(1).
        """
        input_program2 = """

        """
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".lp") as temp_file:
            temp_file.write(input_program1)
            temp_file.flush()
            temp_file_path1 = temp_file.name

        with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".lp") as temp_file:
            temp_file.write(input_program2)
            temp_file.flush()
            temp_file_path2 = temp_file.name

        extensions = [
            TagExtension(),
            ShowExtension(),
        ]
        program_str = transform([temp_file_path1, temp_file_path2], extensions=extensions)
        rsymbols = classic_reify(["--preserve-facts=symtab"], program_str)
        extend_with_theory_symbols(rsymbols)

        expected_symbols = [
            "tag(incremental)",
            "atom_tuple(0)",
            "atom_tuple(0,3)",
            "literal_tuple(0)",
            "literal_tuple(0,1)",
            "literal_tuple(0,2)",
            "rule(disjunction(0),normal(0))",
            'theory_string(0,"mytag")',
            'theory_string(1,"tag_rule")',
            "theory_tuple(0)",
            "theory_tuple(0,0,0)",
            "theory_function(2,1,0)",
            "theory_element_tuple(0)",
            "theory_atom(1,2,0)",
            'theory_string(3,"\\"a(1).\\"")',
            'theory_string(4,"rule_fo")',
            "theory_tuple(1)",
            "theory_tuple(1,0,3)",
            "theory_function(5,4,1)",
            "theory_tuple(2)",
            "theory_tuple(2,0,5)",
            "theory_function(6,1,2)",
            "theory_atom(2,6,0)",
            "literal_tuple(1)",
            "literal_tuple(1,3)",
            "output(a(1),1)",
            "theory_symbol(2,tag_rule(mytag))",
            'theory_symbol(6,tag_rule(rule_fo("a(1).")))',
        ]
        self.assertEqual({str(s) for s in rsymbols}, set(expected_symbols))

        reified_prg = "\n".join([f"{str(s)}." for s in rsymbols])

        reified_prg = extend_reification(reified_out_prg=reified_prg, extensions=extensions)

        self.assertNotIn('theory_string(0,"mytag")', reified_prg)
        self.assertNotIn("literal_tuple(0,2)", reified_prg)
        self.assertIn("tag(rule(disjunction(0),normal(0)),mytag)", reified_prg)
