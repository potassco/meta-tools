"""
The meta_tools project.
"""

import logging
from typing import List
from importlib.resources import path
from clingo import Control
from meta_tools.extensions import ReifyExtension
from clingox.reify import Reifier
from meta_tools.utils.theory import extend_with_theory_symbols

log = logging.getLogger(__name__)


def extend_reification(reified_out_prg: str, extensions: List[ReifyExtension], clean_output: bool = True) -> str:
    ctl = Control(["--warn=none"])
    ctl.add("base", [], reified_out_prg)
    with path("meta_tools.encodings", "extension_show.lp") as encoding:
        log.debug("Loading encoding: %s", encoding)
        ctl.load(str(encoding))
    if clean_output:
        ctl.add("base", [], "#show .")
    for ext in extensions:
        ext.add_extension_encoding(ctl)
    ctl.ground([("base", [])])
    result = []
    with ctl.solve(yield_=True) as handle:
        for model in handle:
            show_atoms = not clean_output
            for sym in model.symbols(shown=True, atoms=show_atoms):
                result.append(str(sym) + ".")
    return "\n".join(result)


def reify_files(
    ctl_args: List[str], file_paths: List[str], extensions: List[ReifyExtension], clean_output: bool = True
) -> str:
    """
    Reify the given files using the provided extensions.

    Args:
        ctl_args (List[str]): The list of clingo control arguments.
        file_paths (List[str]): The list of file paths to reify.
        extensions (List[ReifyExtension]): The list of extensions to use for reification.
        clean_output (bool): Whether to clean the output by hiding non-essential atoms of the reification and auxiliary rules added by the extensions.

    Returns:
        str: The reified program string.
    """
    log.info("Reifying files: %s", file_paths)
    program_string = ""
    ctl = Control(ctl_args + ["--preserve-facts=symtab"])
    # Apply each extension's transformation
    for extension in extensions:
        log.info(f"Applying extension: {extension.__class__.__name__}")
        program_string = extension.transform(file_paths, program_string)
        file_paths = []  # Clear file paths after the first extension
    log.info("Grounding...")

    # Reify
    rsymbols = []
    reifier = Reifier(rsymbols.append, reify_steps=False)
    ctl.register_observer(reifier)
    ctl.add("base", [], program_string)
    ctl.ground([("base", [])])

    # Do we want to have this always?
    extend_with_theory_symbols(rsymbols)
    reified_prg_og = "\n".join([f"{str(s)}." for s in rsymbols])

    # Generate final reified program with theory tags
    with open("out/reified_output_full.lp", "w") as f:
        f.write(reified_prg_og)

    reified_prg = extend_reification(reified_out_prg=reified_prg_og, extensions=extensions, clean_output=clean_output)
    with open("out/reified_output_clean.lp", "w") as f:
        f.write(reified_prg)
    return reified_prg
