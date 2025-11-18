"""
Utility functions for theory handling.
"""

from typing import Callable, Dict, List

from clingo import Function, Number, Symbol, TheoryTermType
from clingox.reify import ReifiedTheory, ReifiedTheoryTerm
from clingox.theory import evaluate, is_operator


def _visit_terms(thy: ReifiedTheory, cb: Callable[[ReifiedTheoryTerm], None]) -> None:
    """
    Visit the terms occuring in the theory atoms of the given theory.

    This function does not recurse into terms.

    Args:
        thy (ReifiedTheory): The reified theory.
        cb (Callable[[ReifiedTheoryTerm], None]): The callback to call for each term
    """
    for atm in thy:
        for elem in atm.elements:
            for term in elem.terms:
                cb(term)
        cb(atm.term)
        guard = atm.guard
        if guard:
            cb(guard[1])  # nocoverage


def _term_symbols(term: ReifiedTheoryTerm, ret: Dict[int, Symbol]) -> None:
    """
    Represent arguments to theory operators using clingo's `clingo.Symbol`
    class.

    Theory terms are evaluated using `clingox.theory.evaluate_unary` and added
    to the given dictionary using the index of the theory term as key.

    Args:
        term (ReifiedTheoryTerm): The theory term to represent.
        ret (Dict[int, Symbol]): The dictionary to add the representation to.
    """
    if term.type == TheoryTermType.Function and is_operator(term.name):
        _term_symbols(term.arguments[0], ret)
        if len(term.arguments) >= 2:
            _term_symbols(term.arguments[1], ret)
    elif term.index not in ret:
        ret[term.index] = evaluate(term)


def extend_with_theory_symbols(symbols: List[Symbol]) -> None:
    """
    Add theory symbols to the given list of symbols.

    The theory symbols are represented using clingo's `clingo.Symbol` class.

    Args:
        symbols (List[Symbol]): The list of symbols to extend.
    """
    theory_symbols: Dict[int, Symbol] = {}
    thy = ReifiedTheory(symbols)
    _visit_terms(thy, lambda term: _term_symbols(term, theory_symbols))

    for k, v in theory_symbols.items():
        symbols.append(Function("theory_symbol", [Number(k), v]))
