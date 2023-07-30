import config
from glob import glob
import multiprocessing
import os
import re
import shutil
import subprocess
from sys import argv


def join_spread(img):
    # "wghjwigh p000 rhjrhhwgjn"
    pattern = r"(.+ p)(\d{3})( .+)"
    m = re.match(pattern, img)
    if m:
        page_right_num = m.group(2)
        page_right = img
        page_left_num = str(int(m.group(2)) + 1).zfill(3)
        page_left = f"{m.group(1)}{page_left_num}{m.group(3)}"
        page_joined = (
            f"{m.group(1)}{page_right_num}-{page_left_num}{m.group(3)[:-4]}.png"
        )
        print(f"[JOIN] {img}")
        subprocess.run(["convert", "+append", page_left, page_right, page_joined])
        # move individual pages of spreads to a subfolder "trash" rather than deleting to prevent some oopsies
        shutil.move(page_right, "trash")
        shutil.move(page_left, "trash")
    else:
        print("unexpected pagename format, failed to join: " + img)


def join_spreads():
    join = argv[1:]
    # absolutely weaponized version of https://stackoverflow.com/a/952952
    imgs = [
        img
        for ext in [glob(f"*.{ext}") for ext in config.ALLOWED_EXTENSIONS]
        for img in ext
    ]
    imgs_to_join = [img for i, img in enumerate(sorted(imgs)) if str(i) in join]
    with multiprocessing.Pool(processes=config.MULTIPROCESSING_CORES) as pool:
        pool.map(join_spread, imgs_to_join)


if __name__ == "__main__":
    if not os.path.isdir("trash"):
        os.mkdir("trash")
    join_spreads()
