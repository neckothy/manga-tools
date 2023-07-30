import argparse
import config
from glob import glob
import os
from PIL import Image
import re
import shutil

parser = argparse.ArgumentParser()
# common special pages (comma-split pages that should be tagged as x)
# not implemented yet cuz I'm dumb & lazy
# parser.add_argument("-aft", "--afterword", help="Afterword")
# parser.add_argument("-cov", "--cover", help="Cover")
# parser.add_argument("-ext", "--extra", help="Extra")
# parser.add_argument("-toc", "--table-of-contents", help="ToC")
# normal stuff
parser.add_argument(
    "-cn",
    "--chapter-numbers",
    help="comma-split chapter numbers, accepts ranges (1..5,5x1)",
)
parser.add_argument("-cp", "--chapter-pages", help="comma-split chapter starting pages")
parser.add_argument(
    "-ct", "--chapter-titles", help="TWO comma-split chapter titles (title,,title2)"
)
parser.add_argument(
    "-d", "--dry-run", help="print output without renaming", action="store_true"
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
    publisher = args.publisher or None
    if publisher and publisher in config.PUBLISHER_SHORTHAND:
        publisher = PUBLISHER_SHORTHAND[publisher]
    info = [title, volume, year, ripper, publisher]
    if title and year and publisher:
        return info
    else:
        print(
            f"missing a required value:\ntitle: {title}\nyear: {year}\npublisher: {publisher}"
        )
        exit()


def get_chapter_index(prev_index, img_index, chap_pages):
    if prev_index == len(chap_pages) - 1:
        return prev_index
    elif img_index < int(chap_pages[prev_index + 1]):
        return prev_index
    elif img_index >= int(chap_pages[prev_index + 1]):
        return prev_index + 1


def rename_pages(title, volume, year, ripper, publisher):
    chap_index = 0

    if args.chapter_numbers and args.chapter_pages:
        chap_nums, chap_pages = [], []
        for num in args.chapter_numbers.split(","):
            rng = re.match(r"(\d{1,4})\.\.(\d{1,4})", num)
            bns = re.match(r"(\d{1,4})(x\d)", num)
            if rng:
                chap_nums.extend(range(int(rng.group(1)), int(rng.group(2)) + 1))
            elif bns:
                chap_nums.append(
                    bns.group(1).zfill(args.chapter_padding) + bns.group(2)
                )
            else:
                chap_nums.append(num)
        chap_pages.extend(args.chapter_pages.split(","))

    # absolutely weaponized version of https://stackoverflow.com/a/952952
    imgs = [
        img
        for ext in [glob(f"*.{ext}") for ext in config.ALLOWED_EXTENSIONS]
        for img in ext
    ]

    for i, img in enumerate(sorted(imgs)):
        # danke danke
        ext = img.rsplit(".", maxsplit=1)[1]
        with Image.open(img) as data:
            w, h = data.size
        if min(w, h) > 1800 and not w > h:
            quality = "{HQ}"
        elif min(w, h) < 900:
            quality = "{LQ}"
        else:
            quality = ""

        if args.chapter_numbers and args.chapter_pages:
            chap_index = get_chapter_index(chap_index, i, chap_pages)
            chap_num = chap_nums[chap_index] if chap_nums and chap_pages else None
        else:
            chap_num = None

        if chap_num:
            chap_title = (
                args.chapter_titles.split(",,")[chap_index]
                if args.chapter_titles
                else None
            )
            new_name = f"{title} - c{str(chap_num).zfill(args.chapter_padding)}"
            if volume:
                new_name += f" (v{volume.zfill(args.volume_padding)})"
            new_name += f" - p{str(i).zfill(3)} [dig]"
            if chap_title:
                new_name += f" [{chap_title}]"
        else:
            new_name = f"{title}"
            if volume:
                new_name += f" (v{volume.zfill(args.volume_padding)})"
            new_name += f" - p{str(i).zfill(3)} [dig]"
        new_name += f" [{publisher}]"
        if ripper:
            new_name += f" [{ripper}]"
        if quality:
            new_name += f" {quality}"
        new_name += f".{ext}"

        if args.dry_run:
            print(f"{img} --> {new_name}")
        else:
            shutil.move(img, new_name)


book_info = get_info()
rename_pages(*book_info)
