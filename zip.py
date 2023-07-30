import argparse
import config
from glob import glob
import os
import re
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--ripper", help="ripper tag")
parser.add_argument("-t", "--title", help="series title")
parser.add_argument(
    "-ts", "--timestamp", help="modified timestamp, defaults to current time"
)
parser.add_argument("-v", "--volume", help="volume number")
parser.add_argument("-y", "--year", help="published year")
parser.add_argument(
    "-vpad",
    "--volume-padding",
    help="zero padding of volume number",
    type=int,
    default=2,
)
args = parser.parse_args()


def get_info():
    ripper = config.RIPPER_TAG if config.RIPPER_TAG != "" else None
    folder = os.path.basename(os.getcwd())
    match = re.match(config.DIRECTORY_PATTERN, folder)
    if match:
        title, volume, year, ripper = match.groups()
    else:
        title, volume, year, ripper = None, None, None, ripper
    title = args.title or title
    volume = args.volume or volume
    year = args.year or year
    ripper = args.ripper or ripper
    info = [title, volume, year, ripper]
    if title and year and ripper:
        return info
    else:
        print(
            f"missing a required value:\ntitle: {title}\nyear: {year}\nripper: {ripper}"
        )
        exit()


def zip_volume(title, volume, year, ripper):
    # idk how to modify timestamps on windows and haven't bothered to look it up
    # https://man.archlinux.org/man/touch.1.en#DATE_STRING
    process_args = (
        ["touch"] if args.timestamp == None else ["touch", "-d", args.timestamp]
    )

    # absolutely weaponized version of https://stackoverflow.com/a/952952
    imgs = [
        img
        for ext in [glob(f"*.{ext}") for ext in config.ALLOWED_EXTENSIONS]
        for img in ext
    ]
    for img in sorted(imgs):
        subprocess.run(process_args + [img])
    if volume:
        archive_name = f"{title} v{volume.zfill(args.volume_padding)} ({year}) (Digital) ({ripper}).cbz"
    else:
        archive_name = f"{title} ({year}) (Digital) ({ripper}).cbz"
    subprocess.run(["7z", "a", "-tzip", "-mtc=off", "-mx=0", archive_name, "./*"])


book_info = get_info()
zip_volume(*book_info)
