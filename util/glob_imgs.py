from glob import glob


def from_allowed_exts(allowed_exts=["jpg", "png"]):
    # https://stackoverflow.com/a/952952
    imgs = [img for ext in [glob(f"*.{ext}") for ext in allowed_exts] for img in ext]
    return sorted(imgs)
