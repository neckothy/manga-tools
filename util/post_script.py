import os
import subprocess


def parse_and_run(args, post_scripts, archive_name):
    for script in post_scripts:
        skip = False
        for i, item in enumerate(script):
            item = item.replace("[[~]]", os.path.expanduser("~"))
            if archive_name:
                item = item.replace("[[cbz]]", archive_name)
            elif not archive_name and "[[cbz]]" in item:
                skip = True
                break
            for k, v in vars(args).items():
                item = item.replace(f"[[{k}]]", str(v))
            script[i] = item
        if not skip:
            if not args.quiet:
                print(f"[POST SCRIPT] {' '.join(script)}")
            subprocess.run(script)
        else:
            if not args.quiet:
                print(f"[POST SCRIPT] SKIPPING {' '.join(script)}")
