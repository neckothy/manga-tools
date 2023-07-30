import argparse
import config
from glob import glob
import multiprocessing
import subprocess


def grayscale_page(img):
    ext = img.rsplit(".", maxsplit=1)[1]
    print(f"[GRAYSCALE] {img}")
    if ext == "jpg":
        subprocess.run(["jpegtran", "-grayscale", "-outfile", img, img])
    if ext == "png":
        subprocess.run(
            [
                "magick",
                "convert",
                img,
                "-format",
                "png",
                "-quality",
                "100",
                "-dither",
                "None",
                "-colorspace",
                "Gray",
                img,
            ]
        )


def grayscale_pages():
    ignored = args.grayscale_ignore.split(",")
    # absolutely weaponized version of https://stackoverflow.com/a/952952
    imgs = [
        img
        for ext in [glob(f"*.{ext}") for ext in config.ALLOWED_EXTENSIONS]
        for img in ext
    ]
    imgs_to_grayscale = [
        img for i, img in enumerate(sorted(imgs)) if str(i) not in ignored
    ]
    with multiprocessing.Pool(processes=config.MULTIPROCESSING_CORES) as pool:
        pool.map(grayscale_page, imgs_to_grayscale)


def denoise_page(img):
    ext = img.rsplit(".", maxsplit=1)[1]
    print(f"[DENOISE] {img}")
    subprocess.run(
        [
            "waifu2x-ncnn-vulkan",
            "-i",
            img,
            "-o",
            img.replace(ext, "png"),
            "-n",
            "1",
            "-s",
            "1",
        ]
    )
    if ext == "jpg":
        subprocess.run(["rm", img])


def denoise_pages():
    ignored = args.denoise_ignore.split(",") if args.denoise_ignore else None
    # absolutely weaponized version of https://stackoverflow.com/a/952952
    imgs = [
        img
        for ext in [glob(f"*.{ext}") for ext in config.ALLOWED_EXTENSIONS]
        for img in ext
    ]
    imgs_to_denoise = [
        img for i, img in enumerate(sorted(imgs)) if str(i) not in ignored
    ]
    # wrote this like the rest but there doesn't seem to be much advantage in multiprocessing this step
    # waifu2x-ncnn-vulkan already uses resources efficiently, or my gpu just isn't powerful enough
    with multiprocessing.Pool(processes=1) as pool:
        pool.map(denoise_page, imgs_to_denoise)


def level_page(img_tup):
    i, img = img_tup
    ignored_gray = args.grayscale_ignore.split(",") if args.grayscale_ignore else None
    ext = img.rsplit(".", maxsplit=1)[1]
    process_args = [
        "convert",
        img,
        "-format",
        "png",
        "-quality",
        "100",
        "-dither",
        "None",
    ]
    if args.grayscale and str(i) not in ignored_gray:
        process_args.extend(["-colorspace", "Gray"])
    if args.level == "auto":
        process_args.append("-auto-level")
    # maybe ok-ish lazy settings for a lot of modern digitals with cmyk conversion issue
    # or whatever it is idk
    # colorblind btw
    if args.level == "generic":
        process_args.extend(["-level", "12.55%,100%,1.25"])
    else:
        process_args.extend(["-level", f"{args.level}"])
    process_args.append(img.replace(ext, "png"))
    print(f"[LEVEL] {img}")
    subprocess.run(process_args)
    if ext == "jpg":
        subprocess.run(["rm", img])


def level_pages():
    ignored = args.level_ignore.split(",") if args.level_ignore else []
    # absolutely weaponized version of https://stackoverflow.com/a/952952
    imgs = [
        img
        for ext in [glob(f"*.{ext}") for ext in config.ALLOWED_EXTENSIONS]
        for img in ext
    ]
    imgs_to_level = [
        (i, img) for i, img in enumerate(sorted(imgs)) if str(i) not in ignored
    ]
    with multiprocessing.Pool(processes=config.MULTIPROCESSING_CORES) as pool:
        pool.map(level_page, imgs_to_level)


def optimize_page(img):
    ext = img.rsplit(".", maxsplit=1)[1]
    print(f"[OPTIMIZE] {img}")
    if ext == "jpg":
        # hehe
        subprocess.run(["wine", config.PINGO_EXE_PATH, "-l", "-s4", "-strip", img])
        # subprocess.run(["jpegtran", "-optimize", "-copy", "none", "-outfile", img, img])
    elif ext == "png":
        subprocess.run(
            ["oxipng", "-o", "6", "-i", "0", "--strip", "all", "--quiet", img]
        )


def optimize_pages():
    # absolutely weaponized version of https://stackoverflow.com/a/952952
    imgs = [
        img
        for ext in [glob(f"*.{ext}") for ext in config.ALLOWED_EXTENSIONS]
        for img in ext
    ]
    # similar to denoise, these tools make pretty good use of resources by default
    # quickly hits diminishing returns (on my machine)
    with multiprocessing.Pool(processes=2) as pool:
        pool.map(optimize_page, imgs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
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
    args = parser.parse_args()

    if args.grayscale:
        grayscale_pages()
    if args.denoise:
        denoise_pages()
    if args.level:
        level_pages()
    if args.optimize:
        optimize_pages()
