# Large opaque PNG art was recompressed to JPG (0.9.6.2). Many paths are built at
# runtime (item icons, building levels, Lanista CG gates) and old saves or mods
# may still name the .png, so a missing "X.png" transparently loads "X.jpg".
# A real X.png (e.g. from a mod) always wins. SDL detects JPEG data by its
# header, so the .png name hint passed to the decoder is harmless.

init -1500 python:

    def _fm_jpg_twin(name):
        if not name.lower().endswith(".png"):
            return None
        if renpy.loader.loadable_core(name):
            return None
        twin = name[:-4] + ".jpg"
        if renpy.loader.loadable_core(twin):
            return twin
        return None

    def _fm_png_open_fallback(name):
        twin = _fm_jpg_twin(name)
        if twin is None:
            return None
        return renpy.loader.load(twin, tl=False)

    def _fm_png_loadable_fallback(name):
        # loadable() hands the callback the unprefixed name; image lookups
        # also search under images/.
        return any(_fm_jpg_twin(prefix + name) is not None for prefix in ("", "images/"))

    config.file_open_callback = _fm_png_open_fallback
    config.loadable_callback = _fm_png_loadable_fallback
