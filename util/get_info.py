import os
import re
import sys


def from_dir_name(args, cwd):
    folder = os.path.basename(cwd)
    match = re.match(args.config_dir_pattern, folder)
    if match:
        title = match.group("title")
        volume = match.group("volume")
        year = match.group("year")
        ripper = match.group("ripper")
    else:
        title, volume, year, ripper = None, None, None, args.config_ripper_tag
    args.title = args.title or title
    args.volume = args.volume or volume
    args.year = args.year or year
    args.ripper = args.ripper or ripper
    args.publisher = args.publisher or None
    if args.publisher and args.publisher in args.config_pub_short:
        args.publisher = args.config_pub_short[args.publisher]

    if args.zip or not args.no_rename:
        if not args.title:
            sys.exit("missing required value for rename/zip: title")

    return args
