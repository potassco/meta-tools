"""
Test cases for main application functionality.
"""

from unittest import TestCase

from meta_tools import classic_reify
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

    def test_theory_symbols(self) -> None:
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
