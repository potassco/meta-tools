"""
The main entry point for the application.
"""

import logging
import sys

from meta_tools import classic_reify, extend_reification, transform
from meta_tools.extensions import ReifyExtension
from meta_tools.extensions.show.show_extension import ShowExtension
from meta_tools.extensions.tag.tag_extension import TagExtension
from meta_tools.utils.logging import configure_logging
from meta_tools.utils.parser import get_parser
from meta_tools.utils.theory import extend_with_theory_symbols
from meta_tools.utils.visualization import visualize_reification

log = logging.getLogger(__name__)


def main() -> None:
    """
    Run the main function.
    """
    extensions = [
        TagExtension(),
        ShowExtension(),
    ]
    parser = get_parser()
    for ext in extensions:
        subparser = parser.add_argument_group(ext.__class__.__name__)
        ext.register_options(subparser)
    args = parser.parse_args()
    configure_logging(sys.stderr, args.log, sys.stderr.isatty())
    log.debug(args)
    const_args = ["-c " + c for c in args.const] if args.const else []

    def save_out(content: str, name: str) -> None:
        if not args.save_out:
            return
        with open(name, "w", encoding="utf-8") as f:
            f.write(content)

    if args.classic:
        extensions = [ReifyExtension()]

    program_str = transform(args.files, extensions=extensions, prg="")
    save_out(program_str, "out/transformed.lp")
    rsymbols = classic_reify(const_args + ["--preserve-facts=symtab"], program_str)
    if not args.classic:
        extend_with_theory_symbols(rsymbols)
    reified_prg = "\n".join([f"{str(s)}." for s in rsymbols])
    save_out(reified_prg, "out/reified_output_full.lp")
    if not args.classic:
        reified_prg = extend_reification(reified_out_prg=reified_prg, extensions=extensions, clean_output=args.clean)
        save_out(reified_prg, "out/reified_output.lp")
    if args.view:
        visualize_reification(reified_prg, open_browser=True)

    sys.stdout.write(reified_prg + "\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
