"""
Visualization utilities for meta_tools using clingraph.
"""

import logging
from importlib.resources import path

from clingo import Control
from clingraph.clingo_utils import ClingraphContext  # type: ignore
from clingraph.graphviz import compute_graphs, render  # type: ignore
from clingraph.orm import Factbase  # type: ignore

log = logging.getLogger(__name__)


def visualize_reification(reified_out_prg: str, open_browser: bool = False) -> None:
    """
    Visualize the reification using clingraph.
    Args:
        reified_out_prg (str): The reified program.
        open_browser (bool, optional): Whether to open the generated file. Defaults to False.
    """
    ctl = Control(["-n1"])
    fbs = []
    ctl = Control(["-n1"])
    ctl.add("base", [], reified_out_prg)
    with path("meta_tools.encodings", "viz.lp") as encoding:
        log.debug("Loading encoding: %s", encoding)
        ctl.load(str(encoding))
    ctl.ground([("base", [])], ClingraphContext())
    ctl.solve(on_model=lambda m: fbs.append(Factbase.from_model(m)))
    graphs = compute_graphs(fbs)
    file = render(graphs, name_format="reification", format="svg", view=open_browser)
    log.debug("Reification visualization saved to: %s", file)
