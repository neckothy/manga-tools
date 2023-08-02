import subprocess
import os


def grayscale_page(i, img, args):
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


def denoise_page(i, img, args):
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
            args.config_denoise_level,
            "-s",
            "1",
        ]
    )
    if ext == "jpg":
        os.remove(img)


def level_page(i, img, args):
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
    grayscale_ignore = (
        args.grayscale_ignore.split(",") if args.grayscale_ignore else None
    )
    if args.grayscale and str(i) not in grayscale_ignore:
        process_args.extend(["-colorspace", "Gray"])
    if args.level == "auto":
        process_args.append("-auto-level")
    if args.level == "generic":
        process_args.extend(["-level", args.config_level_preset])
    else:
        process_args.extend(["-level", args.level])
    process_args.append(img.replace(ext, "png"))
    print(f"[LEVEL] {img}")
    subprocess.run(process_args)
    if ext == "jpg":
        os.remove(img)


def optimize_page(i, img, args):
    ext = img.rsplit(".", maxsplit=1)[1]
    print(f"[OPTIMIZE] {img}")
    if ext == "jpg":
        if os.name == "posix":
            process_args = [
                "wine",
                os.path.expanduser(args.config_pingo_path),
                "-l",
                "-s4",
                "-strip",
                "-quiet",
                img,
            ]
        elif os.name == "nt":
            process_args = ["pingo", "-l", "-s4", "-strip", "-quiet", img]
        subprocess.run(process_args)
    elif ext == "png":
        subprocess.run(
            ["oxipng", "-o", "6", "-i", "0", "--strip", "all", "--quiet", img]
        )
