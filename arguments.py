import argparse


def parse(config):
    parser = argparse.ArgumentParser()

    # clean
    parser.add_argument(
        "-d", "--denoise", help="denoise pages (waifu2x lvl 1)", action="store_true"
    )
    parser.add_argument(
        "-di", "--denoise-ignore", help="pages that shouldn't be denoised"
    )
    parser.add_argument(
        "-g", "--grayscale", help="grayscale pages", action="store_true"
    )
    parser.add_argument(
        "-gi", "--grayscale-ignore", help="pages that shouldn't be grayscaled"
    )
    parser.add_argument(
        "-l",
        "--level",
        help="level pages, expects 'level' value for imagemagick",
    )
    parser.add_argument("-li", "--level-ignore", help="pages that shouldn't be leveled")
    parser.add_argument(
        "-o", "--optimize", help="losslessly optimize pages", action="store_true"
    )

    # rename
    # common special pages (comma-split pages that should be tagged as x)
    # not implemented yet cuz I'm dumb & lazy
    parser.add_argument("-aft", "--afterword", help="Afterword")
    parser.add_argument("-cov", "--cover", help="Cover")
    parser.add_argument("-ext", "--extra", help="Extra")
    parser.add_argument("-toc", "--table-of-contents", help="ToC")
    # normal stuff
    parser.add_argument(
        "-cn",
        "--chapter-numbers",
        help="comma-split chapter numbers, accepts ranges (1..5,5x1)",
    )
    parser.add_argument(
        "-cp", "--chapter-pages", help="comma-split chapter starting pages"
    )
    parser.add_argument(
        "-ct", "--chapter-titles", help="TWO comma-split chapter titles (title,,title2)"
    )
    parser.add_argument(
        "-nr", "--no-rename", help="don't rename images", action="store_true"
    )
    parser.add_argument("-p", "--publisher", help="publisher name")
    parser.add_argument("-r", "--ripper", help="ripper tag")
    parser.add_argument("-t", "--title", help="series title")
    parser.add_argument("-v", "--volume", help="volume number")
    parser.add_argument("-y", "--year", help="published year")
    parser.add_argument(
        "-cpad",
        "--chapter-padding",
        help="zero padding of chapter number",
        type=int,
        default=3,
    )
    parser.add_argument(
        "-vpad",
        "--volume-padding",
        help="zero padding of volume number",
        type=int,
        default=2,
    )
    parser.add_argument(
        "-w", "--web", help="tag [web] instead of [dig]", action="store_true"
    )

    # archive
    parser.add_argument(
        "-z", "--zip", help="create a .cbz of finished imgs", action="store_true"
    )
    parser.add_argument(
        "-ts", "--timestamp", help="modified timestamp, defaults to current time"
    )

    # join
    parser.add_argument(
        "-j",
        "--join",
        help="Join spreads - provide the page numbers of the right-hand page for each spread",
    )

    # delete
    parser.add_argument(
        "-del",
        "--delete-pages",
        help="comma-split list of pages to be removed (from the work folder)",
    )

    parser.add_argument("-q", "--quiet", help="shut up", action="store_true")

    args = parser.parse_args()
    args.config_pingo_path = config.PINGO_EXE_PATH
    args.config_dir_pattern = config.DIRECTORY_PATTERN
    args.config_join_pattern = config.JOIN_PATTERN
    args.config_ripper_tag = config.RIPPER_TAG
    args.config_level_preset = config.LEVEL_PRESET
    args.config_pub_short = config.PUBLISHER_SHORTHAND
    args.config_date_format = config.DATE_FORMAT
    args.config_denoise_level = config.DENOISE_LEVEL

    return args
