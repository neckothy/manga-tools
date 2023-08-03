# scripts will ignore files without the listed extensions to maybe help prevent some oopsies
ALLOWED_EXTENSIONS = ("jpg", "png")

RIPPER_TAG = "tag"

# path to pingo.exe (only used on linux)
# ~ expands to your home directory
PINGO_EXE_PATH = "~/pingo/pingo.exe"

# scripts will attempt to parse some data from the directory name if neeeded
# saves some typing if your "unprepared" folders contain useful info and follow a pattern
# these should overwrite RIPPER_TAG if matched, and should be overwritten by args if supplied
# note that you likely need to modify some of the scripts if you expect to use a modified pattern
# since they expect certain groups to represent certain metadata
# default expects something like "Series Title v01 (2023) (Digital) (Ripper)"
# and is usually referenced as: title, volume, year, ripper = match.groups()
DIRECTORY_PATTERN = r"(.+) v(\d{2,3}) \((\d{4})\) \(Digital\) \((.+)\)"

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

# waifu2x-ncnn-vulkan noise-level arg https://github.com/nihui/waifu2x-ncnn-vulkan#full-usages
# expects a value of -1/0/1/2/3, -1 = no effect (pointless here), 3 = strongest effect
DENOISE_LEVEL = "1"
