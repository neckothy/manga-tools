import subprocess


def zip_volume(args, imgs):
    # idk how to modify timestamps on windows and haven't bothered to look it up
    # https://man.archlinux.org/man/touch.1.en#DATE_STRING
    process_args = ["touch"] if not args.timestamp else ["touch", "-d", args.timestamp]

    for img in imgs:
        subprocess.run(process_args + [img])
    if args.volume:
        archive_name = f"{args.title} v{args.volume.zfill(args.volume_padding)} ({args.year}) (Digital) ({args.ripper}).cbz"
    else:
        archive_name = f"{args.title} ({args.year}) (Digital) ({args.ripper}).cbz"
    subprocess.run(
        ["7z", "a", "-tzip", "-mtc=off", "-mx=0", f"../{archive_name}", "./*"]
    )
