import subprocess
import os
import time


def build_archive_name(args):
    archive_name = args.title
    if args.volume:
        archive_name += f" v{args.volume.zfill(args.volume_padding)}"
    if args.year:
        archive_name += f" ({args.year})"
    archive_name += " (Digital)"
    if args.fix:
        archive_name += f" (F)"
    if args.ripper:
        archive_name += f" ({args.ripper})"
    archive_name += ".cbz"
    return archive_name


def modify_timestamps(args, imgs):
    if os.name == "posix":
        process_args = (
            ["touch"] if not args.timestamp else ["touch", "-d", args.timestamp]
        )

        for img in imgs:
            subprocess.run(process_args + [img])
    elif os.name == "nt":
        modify_time = (
            time.time()
            if not args.timestamp
            else time.mktime(time.strptime(args.timestamp, args.config_date_format))
        )
        for img in imgs:
            os.utime(img, (modify_time, modify_time))


def remove_existing(archive_name, cwd, quiet):
    if os.path.isfile(f"{cwd}/{archive_name}"):
        if not quiet:
            print(f"[ARCHIVE] found existing file {archive_name}")
            print("[ARCHIVE] removing before creating new file")
        os.remove(f"{cwd}/{archive_name}")


def zip_volume(archive_name, cwd):
    subprocess.run(
        ["7z", "a", "-tzip", "-mtc=off", "-mx=0", f"{cwd}/{archive_name}", "./*"]
    )
