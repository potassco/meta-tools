"""
The meta_tools project.
"""

import logging
from importlib.resources import path
from typing import List, Optional, Sequence, Tuple

from clingo import Control, Symbol
from clingox.reify import Reifier

from meta_tools.extensions import ReifyExtension

log = logging.getLogger(__name__)


def extend_reification(reified_out_prg: str, extensions: List[ReifyExtension], clean_output: bool = True) -> str:
    """

    Extend the reification with the given extensions.
    It calls clingo with the reified program and the extension encodings.

    Args:
        reified_out_prg (str): The reified output program.
        extensions (List[ReifyExtension]): The list of extensions to apply.
        clean_output (bool, optional): Whether to clean the output by hiding non-essential atoms. Defaults to True.
        If clean_output is True, it adds a "#show ." directive to hide all atoms
        not explicitly shown by the extensions or the `extension_show.lp` file.

    Returns:
        str: The extended reified program.
    """
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


def classic_reify(
    ctl_args: List[str], program_string: str, programs: Optional[Sequence[tuple[str, Sequence[Symbol]]]] = None
) -> List[Symbol]:
    """
    Reify the given program string using classic reification.

    Args:
        ctl_args (List[str]): The list of control arguments.
        program_string (str): The program string to reify.
        programs (Optional[Tuple[str, List[str]]]): The list of programs to ground. By default is [("base", [])].
    Returns:
        List[Symbol]: The list of symbols defining the reification.
    """
    ctl = Control(ctl_args)
    rsymbols: List[Symbol] = []
    reifier = Reifier(rsymbols.append, reify_steps=False)
    ctl.register_observer(reifier)
    ctl.add("base", [], program_string)
    programs = programs or [("base", [])]
    ctl.ground(programs)
    return rsymbols


def transform(file_paths: List[str], prg: str = "", extensions: Optional[List[ReifyExtension]] = None) -> str:
    """
    Transform the given files using the provided extensions.

    Args:
        file_paths (List[str]): The list of file paths to transform.
        extensions (List[ReifyExtension]): The list of extensions to use for transformation.

    Returns:
        str: The transformed program string.
    """
    extensions = extensions or []
    program_string = prg
    for extension in extensions:
        log.info("Applying transformation for extension: %s", extension.__class__.__name__)
        program_string = extension.transform(file_paths, program_string)
        file_paths = []  # Clear file paths after the first extension
    return program_string
