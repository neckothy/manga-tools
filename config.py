# scripts will ignore files without the listed extensions to maybe help prevent some oopsies
ALLOWED_EXTENSIONS = ("jpg", "png")

RIPPER_TAG = "tag"

# path to pingo.exe (only used on linux)
# ~ expands to your home directory
PINGO_EXE_PATH = "~/pingo/pingo.exe"

# scripts will attempt to parse some data from the directory name if neeeded
# saves some typing if your "unprepared" folders contain useful info and follow a pattern
# these should overwrite RIPPER_TAG if matched, and should be overwritten by args if supplied
# note that you likely need to modify util/get_info.py if you drastically alter this
# default expects something like "Series Title v01 (2023) (Digital) (Ripper)"
DIRECTORY_PATTERN = r"(?P<title>.+) v(?P<volume>\d{2,3}) \((?P<year>\d{4})\) \(Digital\) \((?P<ripper>.+)\)"

# pattern expected when joining pages
JOIN_PATTERN = r"(.+ p)(\d{3})( .+)"

# shortcuts when using --publisher
PUBLISHER_SHORTHAND = {
    "dh": "Dark Horse Comics",
    "d": "DENPA",
    "f": "FAKKU!",
    "gbb": "Glacier Bay Books",
    "ic": "Irodori Comics",
    "jnc": "J-Novel Club",
    "kb": "Kaiten Books",
    "kc": "Kodansha Comics",
    "opb": "One Peace Books",
    "7s": "Seven Seas",
    "se": "Square Enix",
    "sfb": "Star Fruit Books",
    "tp": "TOKYOPOP",
    "vm": "VIZ Media",
    "yp": "Yen Press",
}

# number of processes to be used where applicable
MP_COUNT_DENOISE = 1
MP_COUNT_DELETE = 16
MP_COUNT_GRAYSCALE = 16
MP_COUNT_JOIN = 16
MP_COUNT_LEVEL = 16
MP_COUNT_OPTIMIZE = 2

# arg to substitute when using -level generic
LEVEL_PRESET = "12.55%,100%,1.25"

# expected date format string for modifying timestamps
# https://docs.python.org/3/library/time.html#time.strftime
# windows only, as linux uses `touch -d`
# https://man.archlinux.org/man/touch.1.en#DATE_STRING
# default expects something like "2023-08-24"
DATE_FORMAT = "%Y-%m-%d"

# a LIST of LISTS of argument strings to be executed at the end of this script
# IF --post_scripts is used
# these run from your starting directory, not the work directory
# [[~]] in a string expands to your home directory
# [[cbz]] in a string expands to the finished archive filename
# [[arg]] in a string expands to the given arg, e.g. [[title]] = args.title
# default is just a simple example to clarify structure
POST_SCRIPTS = [
    ["mkdir", "-p", "[[~]]/manga/[[title]]"],
    ["mv", "./[[cbz]]", "[[~]]/manga/[[title]]"],
    ["rm", "-r", "./work"],
]
