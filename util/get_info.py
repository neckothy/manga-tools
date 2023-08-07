import os
import re
import sys


def from_dir_name(args, cwd):
    folder = os.path.basename(cwd)
    match = re.match(args.config_dir_pattern, folder)
    if match:
        title, volume, year, ripper = match.groups()
    else:
        title, volume, year, ripper = None, None, None, args.config_ripper_tag
    args.title = args.title or title
    args.volume = args.volume or volume
    args.year = args.year or year
    args.ripper = args.ripper or ripper
    args.publisher = args.publisher or None
    if args.publisher and args.publisher in args.config_pub_short:
        args.publisher = args.config_pub_short[args.publisher]

    if not args.no_rename and not args.title:
        sys.exit("missing required value for rename: title")

    if args.zip:
        if not all([args.title, args.year, args.ripper]):
            sys.exit("missing one or more required values for zip: title, year, ripper")

    return args
