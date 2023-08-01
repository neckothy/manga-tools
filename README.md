# neck's manga tools
Personal scripts I use for organizing my digital manga purchases.

I mostly read [official digital volumes](https://gist.github.com/neckothy/6654f928fef87529646df3799f5e555a), so the tools in this repo may make some shortsighted assumptions based on that.

### This is written and tested on Linux, and might need some edits to work properly on Windows.

for example:

- `--optimize` ~~always runs pingo in wine~~ should now just expect pingo in path if running Windows
- `--timestamp` ~~relies on `touch`, not sure how this works in Windows~~ should now support modifying time on Windows but with less freedom than Linux (expects `%Y-%m-%d` e.g. `2023-08-01`)
- let me know if you encounter others as I don't have a Windows machine to test on



### This expects to be run within the directory containing your images

---

In addition to any modules in `requirements.txt`, various tools here expect the following in your system PATH:

- `7z`
- `magick`
- `jpegtran`
- `oxipng`
- `pingo` (on Linux `wine` and `pingo.exe` in `~/pingo/`)
- `waifu2x-ncnn-vulkan`

on Arch Linux all requirements can be installed like so:
1. `pacman -S imagemagick libjpeg-turbo oxipng p7zip python-pillow waifu2x-ncnn-vulkan wine`
2. [download](https://css-ig.net/pingo) `pingo-win64.zip`, extract to `~/pingo`

---

**will probably add some actual documentation sometime, in the meantime just look at the code or `-h` I guess, gl**

Quick example:

1. Enter a directory `Yona of the Dawn v39 (2023) (Digital) (Tag)` containing pages `p000.jpg`-`p193.jpg`
2. `python ~/manga-tools/main.py -del 1 -d -di 0 -g -gi 0 -l generic -li 0 -o -cn "223..228,228x1" -cp "3,33,63,95,125,155,181" -ct "The Moment to Put Everything on the Line,,Beyond the Limit,,Exhale,,A Tender Daybreak,,Lurking Under the Cover of Darkness,,Desertion,,Once Upon a Time, in a Land Far Away" -p "VIZ Media" -z -ts "2023-08-01" -j 30` 
3. directory now contains the original pages `p000.jpg`-`p193.jpg`, an archive `Yona of the Dawn v39 (2023) (Digital) (Tag).cbz`, as well as a subdirectory `work` containing the finished pages `Yona of the Dawn - c223 (v39) - p000 [dig] [The Moment to Put Everything on the Line] [VIZ Media] [Tag].jpg`-`Yona of the Dawn - c228x1 (v39) - p192 [dig] [Once Upon a Time, in a Land Far Away] [VIZ Media] [Tag].png`

in the above example (but not necessarily in this listed order):

- the inner cover (originally `p001.jpg`) was deleted
- all pages were denoised, grayscaled, and leveled except for the cover
- the pages were named following something at least close to the Madokami name scheme
- the spread `Yona of the Dawn - c223 (v39) - p030-031 [dig] [The Moment to Put Everything on the Line] [VIZ Media] [Tag].png` was created, and the individual pages removed
- the pages were losslessly optimized
- modified timestamps on the images were changed to the 1st of August, 2023
- the pages were packed to a cbz archive 

It's as "easy" as that!

---

Some related sources which may have helped with or inspired portions of this repo:

- https://github.com/JodanJodan/MangaToolsnke
- https://github.com/noaione/nao-manga-rls
- Madokami Naming Scheme
- Some of my cute manga reading friendos
