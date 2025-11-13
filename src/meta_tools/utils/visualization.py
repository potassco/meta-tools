from importlib.resources import path
from clingo import Control
import logging
from clingraph.orm import Factbase
from clingraph.graphviz import compute_graphs, render
from clingraph.clingo_utils import ClingraphContext

log = logging.getLogger(__name__)


def visualize_reification(reified_out_prg: str, open: bool = False) -> None:
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
    file = render(graphs, name_format="reification", format="svg", view=open)
    log.debug("Reification visualization saved to: %s", file)
