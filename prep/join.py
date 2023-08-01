from os import remove
import re
import subprocess


def join_spread(i, img, args, pattern=r"(.+ p)(\d{3})( .+)"):
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
        subprocess.run(
            ["magick", "convert", "+append", page_left, page_right, page_joined]
        )
        remove(page_right)
        remove(page_left)
    else:
        print("unexpected pagename format, failed to join: " + img)
