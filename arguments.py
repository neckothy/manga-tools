import argparse


def parse(config):
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-q", "--quiet", help="Disable console output of scripts", action="store_true"
    )
    parser.add_argument(
        "-ps",
        "--post-scripts",
        help="Enable run of POST_SCRIPTS as defined in config.py",
        action="store_true",
    )

    # delete
    parser.add_argument(
        "-del",
        "--delete-pages",
        help="Comma-separated list of pages which should be removed",
    )

    # clean
    parser.add_argument(
        "-o",
        "--optimize",
        help="Enable lossless optimization of pages",
        action="store_true",
    )
    parser.add_argument(
        "-d",
        "--denoise",
        help="Enable denoising of pages using DENOISE_LEVEL from config.py",
        action="store_true",
    )
    parser.add_argument(
        "-g", "--grayscale", help="Enable grayscaling of pages", action="store_true"
    )
    parser.add_argument(
        "-l",
        "--level",
        help="Enable leveling of pages using provided value",
    )
    parser.add_argument(
        "-di",
        "--denoise-ignore",
        help="Comma-separated list of pages which shouldn't be denoised",
    )
    parser.add_argument(
        "-gi",
        "--grayscale-ignore",
        help="Comma-separated list of pages which shouldn't be grayscaled",
    )
    parser.add_argument(
        "-li",
        "--level-ignore",
        help="Comma-separated list of pages which shouldn't be leveled",
    )

    # rename
    parser.add_argument(
        "-nr", "--no-rename", help="Disable renaming of pages", action="store_true"
    )
    parser.add_argument(
        "-w",
        "--web",
        help="Use [web] tag on pages rather than [dig]",
        action="store_true",
    )
    parser.add_argument(
        "-cn",
        "--chapter-numbers",
        help="Comma-separated list of chapter numbers, accepts ranges (1..5,5x1)",
    )
    parser.add_argument(
        "-cp", "--chapter-pages", help="Comma-separated list of chapter starting pages"
    )
    parser.add_argument(
        "-ct",
        "--chapter-titles",
        help="TWO comma-separated list of chapter titles (title,,title2)",
    )
    parser.add_argument(
        "-cov",
        "--cover",
        help="Comma separated list of pages which should be tagged [Cover]",
    )
    parser.add_argument(
        "-toc",
        "--table-of-contents",
        help="Comma separated list of pages which should be tagged [ToC]",
    )
    parser.add_argument(
        "-ext",
        "--extra",
        help="Comma separated list of pages which should be tagged [Extra]",
    )
    parser.add_argument(
        "-aft",
        "--afterword",
        help="Comma separated list of pages which should be tagged [Afterword]",
    )
    parser.add_argument(
        "-t", "--title", help="Series title to be used where appropriate"
    )
    parser.add_argument(
        "-v", "--volume", help="Volume number to be used where appropriate"
    )
    parser.add_argument(
        "-y", "--year", help="Publishing year to be used where appropriate"
    )
    parser.add_argument(
        "-p", "--publisher", help="Publisher name to be used where appropriate"
    )
    parser.add_argument(
        "-r", "--ripper", help="Ripper tag to be used where appropriate"
    )
    parser.add_argument(
        "-cpad",
        "--chapter-padding",
        help="Zero-pad chapter number to specified length, default = 3",
        type=int,
        default=3,
    )
    parser.add_argument(
        "-vpad",
        "--volume-padding",
        help="Zero-pad volume number to specified length, default = 2",
        type=int,
        default=2,
    )

    # archive
    parser.add_argument(
        "-z",
        "--zip",
        help="Create a zip (.cbz) archive of finished pages",
        action="store_true",
    )
    parser.add_argument(
        "-ts",
        "--timestamp",
        help="Set access/modify times for finished pages, default = current time",
    )

    # join
    parser.add_argument(
        "-j",
        "--join",
        help="Comma-separated list of spreads which should be joined, use only the lower page number (12,44)",
    )

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
