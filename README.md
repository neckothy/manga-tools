# neck's manga tools
Personal scripts I use for organizing my digital manga purchases. Likely not usable for most people currently, but maybe some parts of it will be useful to someone. I will try to make it more "general" over time, hopefully getting to a sort of clone & run level at some point.

I mostly read [official digital volumes](https://gist.github.com/neckothy/6654f928fef87529646df3799f5e555a), so the tools in this repo may make some shortsighted assumptions based on that.

### This is written and tested on Linux, and definitely needs some edits to work properly on Windows.

for example:

- `--optimize` always runs pingo in wine
- ``--timestamp`` relies on `touch`, not sure how this works in windows
- etc


### This expects to be run within the directory containing your images

---

Some requirements for the various tools here:

- `python-pillow`
- `imagemagick`
- `oxipng`
- `jpegtran`
- `wine`
- `pingo.exe`
- `waifu2x-ncnn-vulkan`
- `7z`

---

**will probably add some actual documentation sometime, in the meantime just look at the code or `-h` I guess, gl**

---

Some related sources which may have helped with portions of this repo:

- https://github.com/JodanJodan/MangaToolsnke
- https://github.com/noaione/nao-manga-rls
- Madokami Naming Scheme
- Some of my cute manga reading friendos
