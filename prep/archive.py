import subprocess
import os
import time


def zip_volume(args, imgs):
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

    archive_name = args.title
    if args.volume:
        archive_name += f" v{args.volume.zfill(args.volume_padding)}"
    archive_name += f" ({args.year}) (Digital)"
    if args.fix:
        archive_name += f" (F)"
    archive_name += f" ({args.ripper}).cbz"

    subprocess.run(
        ["7z", "a", "-tzip", "-mtc=off", "-mx=0", f"../{archive_name}", "./*"]
    )

    return archive_name
