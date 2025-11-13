"""
The main entry point for the application.
"""

import sys
import logging
from meta_tools.utils.logging import configure_logging
from meta_tools.utils.parser import get_parser
from meta_tools.extensions.show.show_extension import ShowExtension
from meta_tools.extensions.tag.tag_extension import TagExtension
from meta_tools import reify_files
from meta_tools.utils.visualization import visualize_reification

log = logging.getLogger(__name__)


def main() -> None:
    """
    Run the main function.
    """
    extensions = [
        ShowExtension(),
        TagExtension(),
    ]
    parser = get_parser()
    for ext in extensions:
        subparser = parser.add_argument_group(ext.__class__.__name__)
        ext.register_options(subparser)
    args = parser.parse_args()
    configure_logging(sys.stderr, args.log, sys.stderr.isatty())
    log.debug(args)
    const_args = ["-c " + c for c in args.const] if args.const else []

    prg = reify_files(const_args, args.files, extensions, args.clean)
    if args.view:
        visualize_reification(prg, open=True)

    sys.stdout.write(prg + "\n")
    exit(0)


if __name__ == "__main__":
    main()
