"""
The main entry point for the application.
"""

from importlib.resources import files
import sys
import logging
from meta_tools.utils.logging import configure_logging
from meta_tools.utils.parser import get_parser
from meta_tools.extensions.show.show_extension import ShowExtension
from meta_tools.extensions.tag.tag_extension import TagExtension
from meta_tools import reify_files, classic_reify
from meta_tools.utils.visualization import visualize_reification
from meta_tools.extensions import ReifyExtension

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

    if args.classic:
        extension = ReifyExtension()
        program_str = extension.transform(args.files, "")
        reified_program = "\n".join([str(s) + "." for s in classic_reify(const_args, program_str)])
    else:
        reified_program = reify_files(const_args, args.files, extensions, args.clean)

    if args.view:
        visualize_reification(reified_program, open=True)

    sys.stdout.write(reified_program + "\n")
    exit(0)


if __name__ == "__main__":
    main()
