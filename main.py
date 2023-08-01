import config
import arguments
from prep import clean, join, rename, archive, delete
from util import glob_imgs

import multiprocessing
import os
import shutil


def make_work_folder(imgs):
    if not os.path.isdir("work"):
        os.mkdir("work")
        for img in imgs:
            shutil.copy(img, f"{os.getcwd()}/work/{img}")
    else:
        print("existing work folder found, using existing images")
    os.chdir("./work")
    imgs = glob_imgs.from_allowed_exts(config.ALLOWED_EXTENSIONS)
    return imgs


def split_work(
    target_func,
    imgs,
    count=config.MP_COUNT,
    ignored=None,
    allowed=None,
    level_guh=False,
):
    # shitty hack for passing needed level args, need to fix betterer
    if level_guh:
        imgs_to_process = [
            (i, img, args.level, args.grayscale, grayscale_ignore)
            for i, img in enumerate(imgs)
            if str(i) not in ignored
        ]
    elif ignored:
        imgs_to_process = [img for i, img in enumerate(imgs) if str(i) not in ignored]
    elif allowed:
        imgs_to_process = [img for i, img in enumerate(imgs) if str(i) in allowed]
    else:
        imgs_to_process = imgs

    with multiprocessing.Pool(processes=count) as pool:
        pool.map(target_func, imgs_to_process)


args = arguments.parse()
imgs = glob_imgs.from_allowed_exts(config.ALLOWED_EXTENSIONS)
if not args.no_rename:
    args = rename.get_info(
        args, config.RIPPER_TAG, config.DIRECTORY_PATTERN, config.PUBLISHER_SHORTHAND
    )

imgs = make_work_folder(imgs)

if args.delete_pages:
    split_work(delete.delete_page, imgs, allowed=args.delete_pages.split(","))
    imgs = glob_imgs.from_allowed_exts(config.ALLOWED_EXTENSIONS)
if not args.no_rename:
    rename.rename_pages(args, imgs)
    imgs = glob_imgs.from_allowed_exts(config.ALLOWED_EXTENSIONS)
if args.grayscale:
    grayscale_ignore = (
        args.grayscale_ignore.split(",") if args.grayscale_ignore else None
    )
    split_work(clean.grayscale_page, imgs, ignored=grayscale_ignore)
if args.denoise:
    denoise_ignore = args.denoise_ignore.split(",") if args.denoise_ignore else None
    split_work(clean.denoise_page, imgs, count=1, ignored=args.denoise_ignore)
    imgs = glob_imgs.from_allowed_exts(config.ALLOWED_EXTENSIONS)
if args.level:
    level_ignore = args.level_ignore.split(",") if args.level_ignore else None
    split_work(clean.level_page, imgs, ignored=args.level_ignore, level_guh=True)
    imgs = glob_imgs.from_allowed_exts(config.ALLOWED_EXTENSIONS)
if args.join:
    split_work(join.join_spread, imgs, allowed=args.join.split(","))
    imgs = glob_imgs.from_allowed_exts(config.ALLOWED_EXTENSIONS)
if args.optimize:
    split_work(clean.optimize_page, imgs, count=2)
if args.zip:
    archive.zip_volume(args, imgs)
