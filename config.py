# scripts will ignore files without the listed extensions to maybe help prevent some oopsies
ALLOWED_EXTENSIONS = ("jpg", "png")

RIPPER_TAG = ""

# scripts will attempt to parse some data from the directory name if neeeded
# saves some typing if your "unprepared" folders contain useful info and follow a pattern
# these should overwrite RIPPER_TAG if matched, and should be overwritten by args if supplied
# note that you likely need to modify some of the scripts if you expect to use a modified pattern
# since they expect certain groups to represent certain metadata
# default expects something like "Series Title v01 (2023) (Digital) (Ripper)"
# and is usually referenced as: title, volume, year, ripper = match.groups()
DIRECTORY_PATTERN = r"(.+) v(\d{2,3}) \((\d{4})\) \(Digital\) \((.+)\)"

# {"s": "Super Cool Publisher", "k": "Kinda Cool Publisher"}
PUBLISHER_SHORTHAND = {}
