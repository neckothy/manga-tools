import os
from PIL import Image
import re
import shutil


def get_info(args, ripper_tag="", dir_pattern="", pub_shorthand={}):
    ripper = ripper_tag if ripper_tag else None
    folder = os.path.basename(os.getcwd())
    match = re.match(dir_pattern, folder)
    if match:
        title, volume, year, ripper = match.groups()
    else:
        title, volume, year, ripper = None, None, None, ripper
    args.title = args.title or title
    args.volume = args.volume or volume
    args.year = args.year or year
    args.ripper = args.ripper or ripper
    args.publisher = args.publisher or None
    if args.publisher and args.publisher in pub_shorthand:
        args.publisher = pub_shorthand[args.publisher]
    if args.title and args.year and args.publisher:
        return args
    else:
        print(
            f"missing a required value:\ntitle: {args.title}\nyear: {args.year}\npublisher: {args.publisher}"
        )
        exit()


def get_chapter_index(prev_index, img_index, chap_pages):
    if prev_index == len(chap_pages) - 1:
        return prev_index
    elif img_index < int(chap_pages[prev_index + 1]):
        return prev_index
    elif img_index >= int(chap_pages[prev_index + 1]):
        return prev_index + 1


def rename_pages(args, imgs):
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

    for i, img in enumerate(imgs):
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
            new_name = f"{args.title} - c{str(chap_num).zfill(args.chapter_padding)}"
            if args.volume:
                new_name += f" (v{args.volume.zfill(args.volume_padding)})"
            new_name += f" - p{str(i).zfill(3)} [dig]"
            if chap_title:
                new_name += f" [{chap_title}]"
        else:
            new_name = f"{args.title}"
            if args.volume:
                new_name += f" (v{args.volume.zfill(args.volume_padding)})"
            new_name += f" - p{str(i).zfill(3)} [dig]"
        new_name += f" [{args.publisher}]"
        if args.ripper:
            new_name += f" [{args.ripper}]"
        if quality:
            new_name += f" {quality}"
        new_name += f".{ext}"

        shutil.move(img, new_name)
