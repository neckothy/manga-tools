import subprocess
from os import remove


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
        remove(img)


# def level_page(img, level):
def level_page(args):
    i, img, level, grayscale, grayscale_ignore = args
    ext = img.rsplit(".", maxsplit=1)[1]
    process_args = [
        "magick",
        "convert",
        img,
        "-format",
        "png",
        "-quality",
        "100",
        "-dither",
        "None",
    ]
    if grayscale and str(i) not in grayscale_ignore:
        process_args.extend(["-colorspace", "Gray"])
    if level == "auto":
        process_args.append("-auto-level")
    # maybe ok-ish lazy settings for a lot of modern digitals with cmyk conversion issue
    # or whatever it is idk
    # colorblind btw
    if level == "generic":
        process_args.extend(["-level", "12.55%,100%,1.25"])
    else:
        process_args.extend(["-level", f"{level}"])
    process_args.append(img.replace(ext, "png"))
    print(f"[LEVEL] {img}")
    subprocess.run(process_args)
    if ext == "jpg":
        remove(img)


def optimize_page(img):
    ext = img.rsplit(".", maxsplit=1)[1]
    print(f"[OPTIMIZE] {img}")
    if ext == "jpg":
        # hehe
        subprocess.run(
            ["wine", "/home/neck/pingo/pingo.exe", "-l", "-s4", "-strip", img]
        )
        # subprocess.run(["jpegtran", "-optimize", "-copy", "none", "-outfile", img, img])
    elif ext == "png":
        subprocess.run(
            ["oxipng", "-o", "6", "-i", "0", "--strip", "all", "--quiet", img]
        )
