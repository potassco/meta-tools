"""
Test cases for main application functionality.
"""

from io import StringIO
from unittest import TestCase
import tempfile

from meta_tools.utils import logging
from meta_tools.utils.logging import configure_logging, get_logger
from meta_tools import classic_reify, transform_files
from meta_tools.extensions.tag.tag_extension import TAG_THEORY, TagExtension
from meta_tools.extensions.show.show_extension import ShowExtension
from meta_tools.utils.theory import extend_with_theory_symbols


GRAMMAR = """
#theory theory {
    term { +  : 6, binary, left;
           <? : 5, binary, left;
           <  : 4, unary };
    &tel/0 : term, any;
    &tel2/0 : term, {=}, term, head
}.
"""


class TestTheory(TestCase):
    """
    Test cases for main application functionality.
    """

    def test_theory_symbols(self):
        """
        Test function to get symbols in a theory.
        """

        prg = GRAMMAR + "&tel { a(s) <? b((2,3)) }."

        symbols = classic_reify([], prg)
        extend_with_theory_symbols(symbols)
        expected_symbols = {
            "theory_symbol(4,a(s))",
            "theory_symbol(9,b((2,3)))",
            "theory_symbol(0,tel)",
        }
        symbols_str = {str(s).rstrip(".") for s in symbols}
        assert expected_symbols.issubset(symbols_str)
